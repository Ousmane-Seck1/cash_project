# Guide d'utilisation — Administrateur Superuser
## Système CASH — Comptabilité Analytique des Services Hospitaliers

---

**Version :** 1.0  
**Public :** Administrateur système (compte superuser)  
**Date :** Mars 2026

---

## Table des matières

1. [Connexion et accès](#1-connexion-et-accès)
2. [Tableau de bord d'accueil](#2-tableau-de-bord-daccueil)
3. [Gestion des hôpitaux](#3-gestion-des-hôpitaux)
4. [Travailler sur un hôpital — le mode staging](#4-travailler-sur-un-hôpital--le-mode-staging)
5. [Gestion des exercices comptables](#5-gestion-des-exercices-comptables)
6. [Gestion du référentiel : Fonctions, Centres, Comptes](#6-gestion-du-référentiel--fonctions-centres-comptes)
7. [Dupliquer la configuration vers tous les hôpitaux](#7-dupliquer-la-configuration-vers-tous-les-hôpitaux)
8. [Résultats et comparaison inter-hôpitaux](#8-résultats-et-comparaison-inter-hôpitaux)
9. [Alertes système](#9-alertes-système)
10. [Bonnes pratiques et sécurité](#10-bonnes-pratiques-et-sécurité)

---

## 1. Connexion et accès

1. Ouvrir le navigateur et accéder à l'URL de l'application.
2. Saisir le **nom d'utilisateur** et le **mot de passe** superuser.
3. Cliquer sur **Se connecter**.

> **Important :** Le compte superuser a accès à **tous les hôpitaux** et à toutes les fonctionnalités d'administration. Ne partagez jamais ces identifiants.

---

## 2. Tableau de bord d'accueil

Après connexion, l'écran d'accueil présente les modules disponibles :

| Carte | Accès |
|-------|-------|
| 🏛️ **Configuration Annuelle** | Exercices, fonctions, centres, comptes |
| 📝 **Saisie mensuelle** | Charges, clés de répartition, produits |
| 📊 **Résultats Analytiques** | Calculs, tableaux, comparaisons |
| 🚪 **Déconnexion** | Fermer la session |

Cliquer sur la carte souhaitée pour accéder au module.

---

## 3. Gestion des hôpitaux

Menu : **Configuration Annuelle → onglet 🏥 Hôpital** (visible uniquement en superuser)

### 3.1 Créer un nouvel hôpital

1. Cliquer sur **➕ Nouveau** pour vider le formulaire.
2. Remplir les champs :
   - **Nom** : nom complet (ex. : Centre Hospitalier Régional de Thiès)
   - **Code** : identifiant court sans espaces (ex. : CHRT)
   - **Adresse**, **Téléphone**, **Email** : informations de contact
3. Cliquer sur **💾 Sauvegarder Hôpital**.

> L'hôpital apparaît immédiatement dans le tableau **Liste des Hôpitaux et Exercices**.

### 3.2 Modifier un hôpital existant

1. Dans le tableau, cliquer sur **Charger** sur la ligne de l'hôpital.
2. Le formulaire se remplit avec les données actuelles.
3. Modifier les champs souhaités.
4. Cliquer sur **💾 Sauvegarder Hôpital**.

### 3.3 Tableau de synthèse des hôpitaux

Le tableau affiche pour chaque hôpital :

| Colonne | Description |
|---------|-------------|
| Nom | Nom complet de l'hôpital |
| Code | Code court |
| Exercices | Nombre total d'exercices créés |
| Exercice actif | Année de l'exercice en cours |
| Actions | Boutons **Charger** et **Dupliquer config** |

---

## 4. Travailler sur un hôpital — le mode staging

Le superuser travaille **hôpital par hôpital**. Toutes les modifications (fonctions, centres, comptes) s'appliquent uniquement à l'hôpital chargé, sans affecter les autres.

### 4.1 Sélectionner l'hôpital de travail

**Méthode A — depuis l'onglet Hôpital :**
1. Dans le tableau, cliquer sur **Charger** sur la ligne de l'hôpital souhaité.
2. L'hôpital devient l'hôpital actif. Tous les onglets (Fonctions, Centres, Comptes) affichent désormais ses données.

**Méthode B — depuis l'onglet Exercice :**
1. Utiliser le sélecteur **Hôpital** en haut de l'onglet.

> **Principe fondamental :** Modifier le référentiel d'un hôpital de référence (ex. : CHRT), puis utiliser **Dupliquer configuration** pour propager vers les autres hôpitaux. Ne pas modifier directement tous les hôpitaux un par un.

---

## 5. Gestion des exercices comptables

Menu : **Configuration Annuelle → onglet 📅 Exercice**

### 5.1 Créer un exercice

1. Sélectionner l'hôpital (sélecteur visible en superuser).
2. Saisir l'**Année** (ex. : 2025).
3. Saisir **Date de début** et **Date de fin**.
4. Sélectionner le **Statut** : Actif / Inactif / Clôturé.
5. Cliquer sur **💾 Sauvegarder**.

### 5.2 Copier depuis l'année précédente

Cette action crée un nouvel exercice en conservant toute la configuration (fonctions, centres, comptes) et en remettant la saisie à zéro.

1. S'assurer qu'une année est sélectionnée dans le formulaire.
2. Cliquer sur **📋 Copier depuis l'année précédente**.
3. Confirmer la clôture de l'exercice en cours et l'ouverture du suivant.

### 5.3 Statuts d'un exercice

| Statut | Signification |
|--------|---------------|
| **Actif** | Exercice en cours — la saisie est ouverte |
| **Inactif** | Exercice suspendu temporairement |
| **Clôturé** | Exercice terminé — aucune modification possible |

---

## 6. Gestion du référentiel : Fonctions, Centres, Comptes

> **Rappel :** Toutes les opérations ci-dessous s'appliquent uniquement à l'**hôpital actuellement chargé**.

### 6.1 Fonctions (onglet 👥 Fonctions)

Les fonctions sont le premier niveau de la nomenclature CASH (ex. : Médical, Administratif, Médico-technique).

**Ajouter une fonction :**
1. Saisir le **Code** (ex. : MED) et le **Libellé** (ex. : Médical).
2. Cliquer sur **➕ Ajouter**.

**Modifier :** Cliquer sur ✏️ sur la ligne de la fonction.  
**Supprimer :** Cliquer sur 🗑️ — attention, cela supprime aussi les centres de responsabilité et de coûts rattachés.

### 6.2 Centres de Responsabilité (onglet 🏢 Centres de Responsabilité)

**Ajouter un centre de responsabilité :**
1. Sélectionner la **Fonction** de rattachement.
2. Saisir le **Code** et le **Libellé**.
3. Cliquer sur **➕ Ajouter**.

### 6.3 Centres de Coûts (onglet 💰 Centres de Coûts)

**Types de centres de coûts :**

| Type | Code | Description |
|------|------|-------------|
| Non tarifaire avec unité d'œuvre | NT_UO | Centre de structure (ex. : blanchisserie) — doit avoir une UO |
| Non tarifaire sans UO | NT_TF | Centre de structure sans UO |
| Centre tarifaire médico-technique | CT_MT | Produit des recettes (ex. : laboratoire) |
| Centre tarifaire clinique | CT_CL | Produit des recettes (ex. : médecine interne) |

**Ajouter un centre de coût :**
1. Saisir le **Code** et le **Libellé**.
2. Sélectionner le **Type de centre**.
3. Saisir l'**Unité d'œuvre** (obligatoire pour NT_UO, CT_MT, CT_CL).
4. Saisir le **Tarif** (obligatoire pour CT_MT et CT_CL).
5. Sélectionner le **Centre de Responsabilité** de rattachement.
6. Saisir l'**Ordre de déversement** si applicable.
7. Cliquer sur **➕ Ajouter**.

### 6.4 Comptes de Charges (onglet 📋 Comptes de Charges)

**Ajouter un compte :**
1. Saisir le **Numéro** (ex. : 6611000) et le **Libellé**.
2. Cliquer sur **➕ Ajouter**.

---

## 7. Dupliquer la configuration vers tous les hôpitaux

Après avoir finalisé le référentiel sur l'hôpital de référence, propager la configuration vers les autres hôpitaux.

### 7.1 Dupliquer depuis l'onglet Hôpital

1. Dans le tableau, cliquer sur **Dupliquer config** sur la ligne de l'**hôpital cible** (celui qui doit recevoir la configuration).
2. Sélectionner l'**hôpital source** dans le menu déroulant.
3. Confirmer l'opération.

> La duplication copie : fonctions, centres de responsabilité, centres de coûts et comptes de charges. Elle ne copie **pas** les données de saisie (charges, produits).

### 7.2 Comportement de la duplication

| Cas | Résultat |
|-----|---------|
| Élément absent dans la cible | Créé |
| Élément déjà présent (même code) | Libellé mis à jour si différent |
| Données de saisie | Non copiées |

---

## 8. Résultats et comparaison inter-hôpitaux

Menu : **Résultats Analytiques**

Le superuser a accès à deux onglets exclusifs :

### 8.1 Comparaison Inter-Hôpitaux

Cet onglet permet de comparer les performances financières de plusieurs hôpitaux sur une même année.

**Utilisation :**
1. Sélectionner l'**Année** souhaitée (ou laisser « Exercice actif / dernier »).
2. Choisir l'**Indicateur principal** : Résultat / Charges / Produits / Marge (%).
3. Dans la liste **Hôpitaux**, maintenir Ctrl (Windows) ou Cmd (Mac) pour sélectionner plusieurs hôpitaux.
4. Cocher **Hôpitaux actifs seulement** si nécessaire.
5. Cliquer sur **Actualiser**.

**Indicateurs synthétiques affichés :**
- Nombre d'hôpitaux comparés
- Résultat total consolidé
- Moyenne du résultat
- Écart max/min
- Nombre d'alertes

**Exports :** Boutons **📥 Export Excel** et **🧾 Export PDF**.

### 8.2 Sélecteur d'hôpital (pilotage global)

En tant que superuser, un sélecteur **Hôpital** et **Exercice** est disponible en haut de la page Résultats pour piloter les données affichées dans tous les onglets.

---

## 9. Alertes système

L'endpoint d'alertes système (`/api/hopitaux/alertes_systeme/`) retourne :

- Hôpitaux sans exercice actif
- Hôpitaux sans compte de charges
- Hôpitaux sans référentiel (fonctions/centres manquants)
- Événements d'audit du jour

> Accessible uniquement via l'API REST. Nécessite le compte superuser.

---

## 10. Bonnes pratiques et sécurité

| Règle | Détail |
|-------|--------|
| Hôpital de référence | Toujours travailler d'abord sur l'hôpital de référence avant de dupliquer |
| Vérification avant duplication | Utiliser l'aperçu (diff) pour voir les écarts avant d'appliquer |
| Sauvegarde | Effectuer une sauvegarde de la base de données avant toute opération en masse |
| Mots de passe | Ne jamais partager les identifiants superuser |
| Clôture d'exercice | Clôturer l'exercice avant d'en ouvrir un nouveau |
| Suppression | Une suppression de fonction entraîne la suppression de tous ses centres de coûts |

---

*Document interne — CASH v1.0 — Confidentiel*
