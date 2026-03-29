# Guide d'utilisation — Configuration Annuelle
## Système CASH — Comptabilité Analytique des Services Hospitaliers

---

**Version :** 1.0  
**Public :** Contrôleur de gestion, Directeur financier, Administrateur hôpital  
**Date :** Mars 2026

---

## Table des matières

1. [Présentation de la configuration annuelle](#1-présentation-de-la-configuration-annuelle)
2. [Accéder à la configuration](#2-accéder-à-la-configuration)
3. [Exercice comptable](#3-exercice-comptable)
4. [Fonctions](#4-fonctions)
5. [Centres de Responsabilité](#5-centres-de-responsabilité)
6. [Centres de Coûts](#6-centres-de-coûts)
7. [Comptes de Charges](#7-comptes-de-charges)
8. [Ordre de saisie recommandé](#8-ordre-de-saisie-recommandé)
9. [Questions fréquentes](#9-questions-fréquentes)

---

## 1. Présentation de la configuration annuelle

La **configuration annuelle** est l'étape préalable à toute saisie. Elle définit le cadre comptable et analytique de votre hôpital pour l'année en cours :

- L'**exercice comptable** (période de référence)
- Les **fonctions** (grandes catégories de l'hôpital)
- Les **centres de responsabilité** (regroupements de services)
- Les **centres de coûts** (unités élémentaires d'analyse)
- Les **comptes de charges** (plan comptable)

> **À faire en début d'année :** La configuration doit être vérifiée et validée avant le début de la saisie mensuelle.

---

## 2. Accéder à la configuration

1. Depuis l'écran d'accueil, cliquer sur la carte **🏛️ Configuration Annuelle**.
2. La page s'ouvre sur l'onglet **📅 Exercice** par défaut.
3. Naviguer entre les onglets en cliquant sur les boutons en haut de page.

**Onglets disponibles :**

| Onglet | Contenu |
|--------|---------|
| 📅 Exercice | Créer et gérer les exercices comptables |
| 👥 Fonctions | Gérer les fonctions de l'hôpital |
| 🏢 Centres de Responsabilité | Gérer les centres de responsabilité |
| 💰 Centres de Coûts | Gérer les centres de coûts |
| 📋 Comptes de Charges | Gérer le plan de comptes |

---

## 3. Exercice comptable

Un **exercice comptable** est la période sur laquelle portent les données de l'année (généralement du 1er janvier au 31 décembre).

### 3.1 Créer un nouvel exercice

1. Cliquer sur l'onglet **📅 Exercice**.
2. Saisir l'**Année** (ex. : 2025).
3. Saisir la **Date de début** (ex. : 01/01/2025) et la **Date de fin** (ex. : 31/12/2025).
4. Sélectionner le **Statut** :
   - **Actif** : exercice en cours, la saisie est ouverte
   - **Inactif** : exercice temporairement suspendu
   - **Clôturé** : exercice terminé
5. Cliquer sur **💾 Sauvegarder**.

### 3.2 Ouvrir un nouvel exercice depuis l'exercice précédent

Pour éviter de re-saisir toute la configuration :

1. S'assurer que l'exercice courant est sélectionné.
2. Cliquer sur **📋 Copier depuis l'année précédente**.
3. Confirmer la clôture de l'exercice courant et l'ouverture du suivant.

> Cette opération **conserve** toute la structure (fonctions, centres, comptes) et **remet à zéro** la saisie (charges, produits, activités).

### 3.3 Liste des exercices

Le tableau en bas de l'onglet affiche tous les exercices de votre hôpital avec leur statut. Cliquer sur une ligne pour la charger dans le formulaire.

### 3.4 Règles importantes

- Il ne peut y avoir qu'**un seul exercice actif** à la fois par hôpital.
- Un exercice clôturé ne peut plus être modifié.
- Avant de clôturer, s'assurer que tous les calculs analytiques ont été lancés.

---

## 4. Fonctions

Les **fonctions** représentent les grandes catégories d'activité de l'hôpital selon la nomenclature CASH.

*Exemples : Médical, Administratif, Hôtellerie, Médico-technique, Logistique*

### 4.1 Ajouter une fonction

1. Cliquer sur l'onglet **👥 Fonctions**.
2. Saisir le **Code** (court, sans espaces, ex. : MED).
3. Saisir le **Libellé** (ex. : Médical).
4. Cliquer sur **➕ Ajouter**.

### 4.2 Modifier une fonction

1. Dans le tableau, cliquer sur le bouton ✏️ de la ligne à modifier.
2. Une fenêtre s'ouvre avec les champs modifiables.
3. Modifier le libellé.
4. Cliquer sur **Enregistrer**.

> **Note :** Le code d'une fonction ne peut pas être modifié après création. Si une erreur de code a été commise, supprimer la fonction et la recréer.

### 4.3 Supprimer une fonction

1. Cliquer sur le bouton 🗑️ de la ligne.
2. Confirmer la suppression.

> **Attention :** La suppression d'une fonction entraîne la suppression en cascade de tous ses **centres de responsabilité** et **centres de coûts** associés.

---

## 5. Centres de Responsabilité

Les **centres de responsabilité** sont des regroupements de services sous une même fonction. Chaque centre de coût appartient à un centre de responsabilité.

*Exemples : Chirurgie (sous Médical), Comptabilité (sous Administratif)*

### 5.1 Ajouter un centre de responsabilité

1. Cliquer sur l'onglet **🏢 Centres de Responsabilité**.
2. Sélectionner la **Fonction** de rattachement dans la liste déroulante.
3. Saisir le **Code** (ex. : CHIR) et le **Libellé** (ex. : Chirurgie).
4. Cliquer sur **➕ Ajouter**.

### 5.2 Modifier un centre de responsabilité

1. Cliquer sur ✏️ dans le tableau.
2. Modifier le libellé ou la fonction.
3. Cliquer sur **Enregistrer**.

> **Note :** Le code d'un centre de responsabilité ne peut pas être modifié après création.

### 5.3 Supprimer un centre de responsabilité

Cliquer sur 🗑️ — cela supprime également tous les **centres de coûts** rattachés.

---

## 6. Centres de Coûts

Les **centres de coûts** sont les unités élémentaires d'analyse de la comptabilité analytique. Chaque charge sera affectée à un centre de coût.

### 6.1 Types de centres de coûts

| Type | Code | Caractéristiques |
|------|------|-----------------|
| Non tarifaire avec UO | **NT_UO** | Centre de structure. Ses charges sont déversées vers d'autres centres selon les clés de répartition. Doit avoir une unité d'œuvre. |
| Non tarifaire sans UO | **NT_TF** | Centre de structure. Ses charges sont déversées selon un forfait. |
| Tarifaire médico-technique | **CT_MT** | Centre qui génère des recettes (ex. : laboratoire, radiologie). Doit avoir une unité d'œuvre et un tarif. |
| Tarifaire clinique | **CT_CL** | Centre qui génère des recettes (ex. : médecine interne, pédiatrie). Doit avoir une unité d'œuvre et un tarif. |

### 6.2 Ajouter un centre de coût

1. Cliquer sur l'onglet **💰 Centres de Coûts**.
2. Remplir les champs :
   - **Code** : identifiant court (ex. : LABO)
   - **Libellé** : nom complet (ex. : Laboratoire d'analyses)
   - **Type de centre** : sélectionner dans la liste
   - **Centre de Responsabilité** : rattachement hiérarchique
   - **Unité d'œuvre** : nature de l'activité mesurée (ex. : journée, acte, dossier) — obligatoire pour NT_UO, CT_MT, CT_CL
   - **Tarif** : prix unitaire — obligatoire pour CT_MT et CT_CL
   - **Ordre de déversement** : rang dans la cascade de déversement (pour NT_TF uniquement)
3. Cliquer sur **➕ Ajouter**.

### 6.3 Modifier un centre de coût

Cliquer sur ✏️ — tous les champs (libellé, type, UO, tarif, ordre) sont modifiables sauf le **code** et le **centre de responsabilité**.

### 6.4 Tableau récapitulatif

Le tableau affiche tous les centres de coûts avec :
- Code, Libellé, Type
- Unité d'œuvre, Tarif
- Centre de Responsabilité de rattachement
- Ordre de déversement

---

## 7. Comptes de Charges

Les **comptes de charges** correspondent au plan comptable de l'hôpital. Chaque charge saisie est associée à un compte.

*Exemples : 6611 — Rémunérations, 6064 — Fournitures médicales*

### 7.1 Ajouter un compte

1. Cliquer sur l'onglet **📋 Comptes de Charges**.
2. Saisir le **Numéro** (ex. : 6611000).
3. Saisir le **Libellé** (ex. : Rémunérations du personnel médical).
4. Cliquer sur **➕ Ajouter**.

### 7.2 Modifier un compte

Cliquer sur ✏️ — le libellé est modifiable. Le numéro de compte est fixe après création.

### 7.3 Supprimer un compte

Cliquer sur 🗑️ — uniquement si aucune charge n'est associée à ce compte.

---

## 8. Ordre de saisie recommandé

Pour éviter les dépendances manquantes, respecter cet ordre lors de la création initiale :

```
1. Exercice comptable
       ↓
2. Fonctions
       ↓
3. Centres de Responsabilité  (rattachés aux fonctions)
       ↓
4. Centres de Coûts  (rattachés aux centres de responsabilité)
       ↓
5. Comptes de Charges  (indépendants)
```

> Une fois la configuration validée, avertir le comptable qu'il peut commencer la saisie mensuelle.

---

## 9. Questions fréquentes

**Q : Peut-on modifier le code d'une fonction ou d'un centre après création ?**  
Non. En cas d'erreur, supprimer l'élément et le recréer avec le bon code.

**Q : Peut-on avoir plusieurs exercices actifs en même temps ?**  
Non. Un seul exercice peut être actif à la fois par hôpital.

**Q : Que se passe-t-il si on supprime un centre de coût auquel des charges ont été affectées ?**  
La suppression sera bloquée si des charges sont associées. Réaffecter les charges avant de supprimer.

**Q : Comment savoir si la configuration est complète avant de commencer la saisie ?**  
Vérifier que les éléments suivants sont présents :
- Au moins un exercice actif
- Au moins une fonction
- Au moins un centre de responsabilité
- Au moins un centre de coût par type (NT_UO pour la répartition)
- Les comptes de charges correspondant au plan comptable

---

*Document interne — CASH v1.0 — Confidentiel*
