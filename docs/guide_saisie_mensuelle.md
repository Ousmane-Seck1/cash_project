# Guide d'utilisation — Saisie Mensuelle
## Système CASH — Comptabilité Analytique des Services Hospitaliers

---

**Version :** 1.0  
**Public :** Comptable, Contrôleur de gestion  
**Date :** Mars 2026

---

## Table des matières

1. [Présentation de la saisie mensuelle](#1-présentation-de-la-saisie-mensuelle)
2. [Accéder à la saisie](#2-accéder-à-la-saisie)
3. [Saisie des charges](#3-saisie-des-charges)
4. [Clés de répartition](#4-clés-de-répartition)
5. [Saisie des produits (Recettes)](#5-saisie-des-produits-recettes)
6. [Saisie des activités](#6-saisie-des-activités)
7. [Ordre de saisie recommandé](#7-ordre-de-saisie-recommandé)
8. [Corrections et suppressions](#8-corrections-et-suppressions)
9. [Questions fréquentes](#9-questions-fréquentes)

---

## 1. Présentation de la saisie mensuelle

La **saisie mensuelle** consiste à enregistrer chaque mois les données nécessaires au calcul analytique :

| Module | Qui saisit | Fréquence |
|--------|-----------|-----------|
| **Charges** | Comptable | Mensuelle — après clôture comptable |
| **Clés de répartition** | Contrôleur de gestion | Une fois par an (ou si changement) |
| **Produits (Recettes)** | Comptable / Contrôleur | Mensuelle |
| **Activités** | Contrôleur de gestion | Mensuelle |

> **Prérequis :** La configuration annuelle (exercice, fonctions, centres, comptes) doit être complète avant de commencer la saisie.

---

## 2. Accéder à la saisie

1. Depuis l'écran d'accueil, cliquer sur la carte **📝 Saisie mensuelle**.
2. La page s'ouvre sur l'onglet **💰 Charges** par défaut.
3. Les données affichées correspondent à l'exercice actif de votre hôpital.

**Onglets disponibles :**

| Onglet | Contenu |
|--------|---------|
| 💰 Charges | Saisie et liste des charges imputées |
| 🔑 Clés de Répartition | Définir les clés pour les centres NT_UO |
| 💵 Produits | Saisie des recettes par centre tarifaire |
| 📊 Activités | Saisie des volumes d'activité |

---

## 3. Saisie des charges

L'onglet **Charges** permet d'enregistrer toutes les dépenses de l'hôpital et de les affecter à un centre de coût.

### 3.1 Saisir une nouvelle charge

1. Cliquer sur l'onglet **💰 Charges**.
2. Remplir le formulaire :

| Champ | Description | Obligatoire |
|-------|-------------|-------------|
| **Date** | Date de la pièce comptable | Oui |
| **N° BE/BC** | Numéro du bon d'entrée ou bon de commande | Non |
| **N° OP** | Numéro de l'opération comptable | Non |
| **Désignation** | Description de la dépense | Oui |
| **Compte de charges** | Compte du plan comptable (ex. : 6611000) | Oui |
| **Centre de Responsabilité** | Filtre pour affiner la liste des centres de coûts | Non |
| **Centre de Coût** | Centre auquel la charge est imputée | Oui |
| **Montant** | Montant en francs CFA | Oui |

3. Cliquer sur **💾 Enregistrer**.

> La charge apparaît immédiatement dans le tableau en bas de page.

### 3.2 Astuces pour la saisie

- Utiliser le **filtre Centre de Responsabilité** pour réduire la liste des centres de coûts et retrouver plus facilement le bon centre.
- Le champ **N° BE/BC** et **N° OP** permettent la traçabilité avec la comptabilité générale — les remplir si disponible.
- Saisir toutes les charges du mois avant de les envoyer au calcul.

### 3.3 Tableau des charges

Le tableau affiche les colonnes : **Date**, **Compte**, **Désignation**, **Centre de coût**, **Montant**, **Actions**.

Utilisez le bouton ✏️ pour modifier une charge ou 🗑️ pour la supprimer.

---

## 4. Clés de répartition

Les **clés de répartition** définissent comment les charges des **centres de structure (NT_UO)** sont réparties vers les autres centres.

> **Exemple :** La blanchisserie (NT_UO) est répartie à 40% vers Médecine, 35% vers Chirurgie et 25% vers Maternité.

### 4.1 Principe de fonctionnement

- Chaque centre NT_UO doit avoir des clés qui totalisent **exactement 100%**.
- Les centres de destination peuvent être de n'importe quel type.
- Les clés sont généralement définies **une fois par an** et restent valables toute l'année sauf changement organisationnel.

### 4.2 Définir les clés d'un centre source

1. Cliquer sur l'onglet **🔑 Clés de Répartition**.
2. Sélectionner le **Centre de Coût Source** (le centre NT_UO à répartir).
3. Le formulaire de saisie des clés apparaît, avec une **barre de progression** indiquant le total actuel.

**Ajouter une clé :**
1. Sélectionner éventuellement un **Filtre par Centre de Resp. (Destination)** pour affiner la liste.
2. Sélectionner le **Centre de Coût de destination**.
3. Saisir le **Pourcentage** (ex. : 40).
4. Cliquer sur **➕ Ajouter**.
5. Répéter pour chaque centre de destination.

**Enregistrer la répartition :**
Quand le total atteint **100%** (barre verte), cliquer sur **✅ Enregistrer la répartition**.

> Si le total dépasse 100%, les nouvelles clés sont bloquées. Modifier ou supprimer des clés existantes pour ajuster.

### 4.3 Modifier ou supprimer une clé

Dans le tableau des clés du centre sélectionné :
- Cliquer sur ✏️ pour modifier le pourcentage.
- Cliquer sur 🗑️ pour supprimer une clé.

Après suppression, saisir les nouvelles clés et enregistrer.

---

## 5. Saisie des produits (Recettes)

L'onglet **Produits** permet d'enregistrer les recettes générées par les **centres tarifaires** (CT_MT et CT_CL).

### 5.1 Saisir un produit (recette)

1. Cliquer sur l'onglet **💵 Produits**.
2. Sélectionner le **Centre de Responsabilité** pour filtrer la liste des centres tarifaires.
3. Sélectionner le **Centre Tarifaire** (CT_MT ou CT_CL uniquement).
4. Saisir le **Montant** des recettes pour la période.
5. Sélectionner le **Type de produit** :

| Type | Description |
|------|-------------|
| Produits ordinaires | Recettes courantes d'exploitation |
| Produits suppletifs | Recettes supplémentaires |
| Autres produits | Produits divers |
| Subvention d'exploitation | Subventions reçues |
| Autres subventions | Autres formes de subventions |

6. Sélectionner la **Période** (mois de janvier à décembre).
7. Cliquer sur **💾 Enregistrer**.

### 5.2 Tableau des produits

Le tableau affiche : **Centre de Coût**, **Type**, **Période**, **Montant**, **Actions**.

---

## 6. Saisie des activités

L'onglet **Activités** permet d'enregistrer les **volumes d'activité** des centres tarifaires, indispensables au calcul du Coût de Revient Unitaire (CRU).

> **Exemple :** Le laboratoire (CT_MT) a réalisé 1 250 actes en janvier.

### 6.1 Saisir une activité

1. Cliquer sur l'onglet **📊 Activités**.
2. Sélectionner le **Centre de Responsabilité** pour filtrer.
3. Sélectionner le **Centre Tarifaire** (CT_MT ou CT_CL).
4. Vérifier l'**Unité d'œuvre** (affichée automatiquement selon le centre — ex. : acte, journée, dossier).
5. Saisir le **Volume des activités** pour la période (nombre entier ou décimal).
6. Sélectionner la **Période** (mois).
7. Cliquer sur **💾 Enregistrer**.

### 6.2 Tableau des activités

Le tableau affiche : **Centre de Coût**, **Unité d'œuvre**, **Volume**, **Période**, **Actions**.

---

## 7. Ordre de saisie recommandé

Pour un mois donné, respecter cet ordre :

```
1. Charges  (imputer toutes les dépenses du mois)
       ↓
2. Clés de répartition  (vérifier/mettre à jour si nécessaire)
       ↓
3. Produits/Recettes  (enregistrer les recettes du mois)
       ↓
4. Activités  (enregistrer les volumes d'activité du mois)
       ↓
5. Lancer le calcul analytique  (depuis Résultats Analytiques)
```

---

## 8. Corrections et suppressions

### 8.1 Modifier une entrée

1. Dans le tableau concerné, cliquer sur ✏️ sur la ligne à modifier.
2. Une fenêtre s'ouvre avec les champs modifiables.
3. Corriger les valeurs.
4. Cliquer sur **Enregistrer**.

### 8.2 Supprimer une entrée

1. Cliquer sur 🗑️ sur la ligne à supprimer.
2. Confirmer la suppression.

> **Attention :** La suppression d'une charge ou d'un produit est **définitive**. Vérifier avant de confirmer.

### 8.3 Cas d'une saisie sur le mauvais mois

1. Supprimer l'entrée erronée.
2. La re-saisir avec la bonne période.

---

## 9. Questions fréquentes

**Q : Je ne vois pas le centre de coût que je recherche dans la liste.**  
Vérifier que le centre de coût a bien été créé dans la Configuration Annuelle. S'il s'agit d'un nouveau centre, contacter l'administrateur pour qu'il soit ajouté.

**Q : Le total de mes clés de répartition ne fait pas 100% — que se passe-t-il ?**  
Le calcul analytique sera bloqué ou donnera des résultats incorrects. S'assurer que toutes les clés d'un centre source totalisent exactement 100% avant de lancer le calcul.

**Q : Peut-on saisir les charges de plusieurs mois en même temps ?**  
Oui. Le champ **Date** permet de saisir n'importe quelle date dans la période de l'exercice actif.

**Q : Peut-on modifier des données après le calcul analytique ?**  
Oui, mais il faudra **relancer le calcul** pour mettre à jour les résultats.

**Q : La liste des comptes de charges est vide.**  
La configuration annuelle n'a pas encore été effectuée. Contacter l'administrateur pour créer les comptes de charges.

---

*Document interne — CASH v1.0 — Confidentiel*
