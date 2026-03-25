
"""Moteur de calcul pour la Comptabilité Analytique Hospitalière

Impémente la logique de répartition primaire et secondaire.
"""
from collections import defaultdict

import pandas as pd
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from .models import (
    Charge, CentreCout, CleRepartition, Activite, Produit,
    ResultatCalcul, Exercice
)


class MoteurCalculCAH:
    """
    Moteur de calcul de la comptabilité analytique hospitalière.
    
    Implémente les 4 étapes du calcul :
    1. Répartition primaire : agrégation des charges par centre
    2. Répartition secondaire 1 : déversement des centres NT_UO selon clés
    3. Répartition secondaire 2 : cascade des centres NT_TF
    4. Calcul final : coûts de revient et résultats analytiques
    """
    
    def __init__(self, exercice_id):
        self.exercice = Exercice.objects.get(id=exercice_id)
        self.resultats = {}
        
    def calculer_tout(self):
        """Exécute le calcul complet de la CAH"""
        print(f"Démarrage du calcul pour l'exercice {self.exercice.annee}")
        
        # Étape 1 : Répartition primaire
        self._repartition_primaire()
        
        # Étape 2 : Répartition secondaire 1 (NT_UO)
        self._repartition_secondaire_1()
        
        # Étape 3 : Répartition secondaire 2 (NT_TF - cascade)
        self._repartition_secondaire_2()
        
        # Étape 4 : Calcul final (coûts de revient, résultats)
        self._calcul_final()
        
        # Sauvegarde des résultats
        self._sauvegarder_resultats()
        
        return self.resultats
    
    def _repartition_primaire(self):
        """
        Étape 1 : Agrégation des charges saisies par centre de coût
        """
        print("Étape 1 : Répartition primaire")
        
        # Récupération de toutes les charges de l'exercice
        charges = Charge.objects.filter(exercice=self.exercice)
        
        # Agrégation par centre de coût
        charges_par_centre = charges.values('centre_cout').annotate(
            total=Sum('montant')
        )
        
        # Initialisation des résultats
        for item in charges_par_centre:
            centre_id = item['centre_cout']
            montant = item['total'] or Decimal('0')
            
            if centre_id not in self.resultats:
                self.resultats[centre_id] = {
                    'charges_directes': Decimal('0'),
                    'charges_indirectes': Decimal('0'),
                    'charges_totales': Decimal('0'),
                }
            
            self.resultats[centre_id]['charges_directes'] = montant
            self.resultats[centre_id]['charges_totales'] = montant
        
        print(f"  → {len(charges_par_centre)} centres avec charges directes")
    
    def _repartition_secondaire_1(self):
        """
        Étape 2 : Répartition des centres NT_UO selon les clés de répartition
        Les charges des centres NT_UO sont réparties aux autres centres
        """
        print("Étape 2 : Répartition secondaire 1 (NT_UO)")
        
        # Récupération des centres NT_UO
        centres_nt_uo = CentreCout.objects.filter(
            type_centre='NT_UO',
            est_actif=True
        )
        
        for centre_uo in centres_nt_uo:
            centre_id = centre_uo.id
            
            # Vérifier si ce centre a des charges
            if centre_id not in self.resultats:
                continue
                
            charges_a_repartir = self.resultats[centre_id]['charges_totales']
            
            if charges_a_repartir <= 0:
                continue
            
            # Récupération des clés de répartition
            cles = CleRepartition.objects.filter(
                exercice=self.exercice,
                centre_source=centre_uo
            )
            
            if not cles:
                raise ValueError(f"Pas de clé de répartition définie pour le centre NT_UO '{centre_uo.code}'.")

            # Vérification que le total fait 100%
            total_pourcentage = sum(c.pourcentage for c in cles)
            
            if total_pourcentage != 100:
                raise ValueError(f"Répartition invalide pour centre NT_UO '{centre_uo.code}' : total clés = {total_pourcentage}%. Doit être 100%.")

            # Répartition
            for cle in cles:
                destination_id = cle.centre_destination.id
                montant_reparti = charges_a_repartir * (cle.pourcentage / 100)
                
                # Initialiser le centre destination si nécessaire
                if destination_id not in self.resultats:
                    self.resultats[destination_id] = {
                        'charges_directes': Decimal('0'),
                        'charges_indirectes': Decimal('0'),
                        'charges_totales': Decimal('0'),
                    }
                
                # Ajouter les charges indirectes
                self.resultats[destination_id]['charges_indirectes'] += montant_reparti
                self.resultats[destination_id]['charges_totales'] += montant_reparti
            
            # Le centre NT_UO est maintenant à zéro (charges totalement déversées)
            self.resultats[centre_id]['charges_indirectes'] = Decimal('0')
            self.resultats[centre_id]['charges_totales'] = Decimal('0')
            
            print(f"  → {centre_uo.code}: {charges_a_repartir} répartis")
    
    def _repartition_secondaire_2(self):
        """
        Étape 3 : Répartition des centres NT_TF par méthode cascade (escalier)
        Chaque centre NT_TF déverse ses charges vers les centres tarifaires
        (CT_MT / CT_CL) proportionnellement à leurs charges totales.
        Un centre tarifaire avec base nulle ne reçoit rien.
        """
        print("Étape 3 : Répartition secondaire 2 (NT_TF - cascade)")
        
        # Récupération des centres NT_TF ordonnés
        centres_nt_tf = CentreCout.objects.filter(
            type_centre='NT_TF',
            est_actif=True
        ).order_by('ordre_cascade')

        centres_tarifaires = list(CentreCout.objects.filter(
            type_centre__in=['CT_MT', 'CT_CL'],
            est_actif=True
        ))
        
        for i, centre_tf in enumerate(centres_nt_tf):
            centre_id = centre_tf.id
            
            # Vérifier si ce centre a des charges (directes + indirectes reçues)
            if centre_id not in self.resultats:
                continue
            
            charges_a_repartir = self.resultats[centre_id]['charges_totales']
            
            if charges_a_repartir <= 0:
                continue
            
            # Les centres receveurs sont uniquement les centres tarifaires
            # avec une base strictement positive.
            centres_destinations = []
            base_calcul = Decimal('0')

            for dest in centres_tarifaires:
                base_dest = self.resultats.get(dest.id, {}).get('charges_totales', Decimal('0'))
                if base_dest > 0:
                    centres_destinations.append((dest, base_dest))
                    base_calcul += base_dest
            
            if base_calcul <= 0:
                print(f"  ⚠️  Centre {centre_tf.code}: base de calcul nulle")
                continue
            
            taux_frais = charges_a_repartir / base_calcul
            
            # Répartition
            for dest, base_dest in centres_destinations:
                if dest.id not in self.resultats:
                    self.resultats[dest.id] = {
                        'charges_directes': Decimal('0'),
                        'charges_indirectes': Decimal('0'),
                        'charges_totales': Decimal('0'),
                    }

                montant_reparti = base_dest * taux_frais
                
                self.resultats[dest.id]['charges_indirectes'] += montant_reparti
                self.resultats[dest.id]['charges_totales'] += montant_reparti
            
            # Le centre NT_TF est maintenant à zéro
            self.resultats[centre_id]['charges_indirectes'] = Decimal('0')
            self.resultats[centre_id]['charges_totales'] = Decimal('0')
            
            print(f"  → {centre_tf.code}: {charges_a_repartir} répartis (taux: {taux_frais:.4f})")
    
    def _calcul_final(self):
        """
        Étape 4 : Calcul des coûts de revient et résultats analytiques
        """
        print("Étape 4 : Calcul final")
        
        # Récupération des activités et produits
        activites = defaultdict(lambda: Decimal('0'))
        for activite in Activite.objects.filter(exercice=self.exercice):
            activites[activite.centre_cout_id] += activite.volume
        
        produits = defaultdict(lambda: Decimal('0'))
        for produit in Produit.objects.filter(exercice=self.exercice):
            produits[produit.centre_cout_id] += produit.montant
        
        for centre_id, data in self.resultats.items():
            centre = CentreCout.objects.get(id=centre_id)
            
            # Pour les centres tarifaires, calculer le coût de revient
            if centre.type_centre in ['CT_MT', 'CT_CL']:
                volume = activites.get(centre_id, Decimal('0'))
                produit = produits.get(centre_id, Decimal('0'))
                
                data['volume_activite'] = volume
                data['produits'] = produit
                
                if volume > 0:
                    data['cout_revient_unitaire'] = data['charges_totales'] / volume
                else:
                    data['cout_revient_unitaire'] = None
                
                data['resultat_analytique'] = produit - data['charges_totales']
    
    def _sauvegarder_resultats(self):
        """Sauvegarde des résultats en base de données"""
        print("Sauvegarde des résultats...")
        
        with transaction.atomic():
            # Supprimer les anciens résultats
            ResultatCalcul.objects.filter(exercice=self.exercice).delete()
            
            # Créer les nouveaux
            for centre_id, data in self.resultats.items():
                ResultatCalcul.objects.create(
                    exercice=self.exercice,
                    centre_cout_id=centre_id,
                    charges_directes=data.get('charges_directes', 0),
                    charges_indirectes=data.get('charges_indirectes', 0),
                    charges_totales=data['charges_totales'],
                    produits=data.get('produits'),
                    volume_activite=data.get('volume_activite'),
                    cout_revient_unitaire=data.get('cout_revient_unitaire'),
                    resultat_analytique=data.get('resultat_analytique')
                )
        
        print(f"✅ {len(self.resultats)} résultats sauvegardés")
    
    def get_tableau_resultats(self):
        """Retourne les résultats sous forme de DataFrame pour export"""
        resultats = ResultatCalcul.objects.filter(
            exercice=self.exercice
        ).select_related('centre_cout')
        
        data = []
        for r in resultats:
            data.append({
                'Code': r.centre_cout.code,
                'Libellé': r.centre_cout.libelle,
                'Type': r.centre_cout.get_type_centre_display(),
                'Charges Directes': r.charges_directes,
                'Charges Indirectes': r.charges_indirectes,
                'Charges Totales': r.charges_totales,
                'Produits': r.produits or 0,
                'Volume': r.volume_activite or 0,
                'Coût Unitaire': r.cout_revient_unitaire or 0,
                'Résultat': r.resultat_analytique or 0,
            })
        
        return pd.DataFrame(data)
