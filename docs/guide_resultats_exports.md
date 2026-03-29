# Guide d'utilisation — Résultats Analytiques et Exports
## Système CASH — Comptabilité Analytique des Services Hospitaliers

---

**Version :** 1.0  
**Public :** Directeur, Responsable financier, Contrôleur de gestion, Superuser  
**Date :** Mars 2026

---

## Table des matières

1. [Présentation des résultats analytiques](#1-présentation-des-résultats-analytiques)
2. [Accéder aux résultats](#2-accéder-aux-résultats)
3. [Lancer le calcul analytique](#3-lancer-le-calcul-analytique)
4. [Résultats par Centre de Coût](#4-résultats-par-centre-de-coût)
5. [Résultats par Centre de Responsabilité](#5-résultats-par-centre-de-responsabilité)
6. [Comparaison Tarif vs Coût de Revient Unitaire](#6-comparaison-tarif-vs-coût-de-revient-unitaire)
7. [Charges Détaillées](#7-charges-détaillées)
8. [Dashboard](#8-dashboard)
9. [Évolution sur plusieurs années](#9-évolution-sur-plusieurs-années)
10. [Comparaison Inter-Hôpitaux (Superuser)](#10-comparaison-inter-hôpitaux-superuser)
11. [Exports Excel et PDF](#11-exports-excel-et-pdf)
12. [Lecture et interprétation des résultats](#12-lecture-et-interprétation-des-résultats)

---

## 1. Présentation des résultats analytiques

Le module **Résultats Analytiques** est le cœur décisionnel du système CASH. Il produit, à partir des données saisies, les indicateurs de performance par centre d'activité.

**Le calcul analytique effectue automatiquement :**

1. **Répartition primaire** — imputation des charges directes sur chaque centre de coût
2. **Répartition secondaire 1** — déversement des centres NT_UO selon les clés de répartition
3. **Répartition secondaire 2** — second déversement si nécessaire
4. **Calcul des résultats** — charges totales, produits, résultats, CRU par centre

---

## 2. Accéder aux résultats

1. Depuis l'écran d'accueil, cliquer sur la carte **📊 Résultats Analytiques**.
2. Si vous êtes **superuser**, sélectionner d'abord l'**hôpital** et l'**exercice** dans le sélecteur en haut de page.
3. Naviguer entre les onglets pour accéder aux différents tableaux.

**Onglets disponibles :**

| Onglet | Accès | Description |
|--------|-------|-------------|
| 🧮 Lancer Calcul | Tous | Déclencher le calcul analytique |
| 📋 Résultats Centre de Coût | Tous | Tableau complet par centre |
| 🏢 Résultats Centre de Resp. | Tous | Tableau par centre de responsabilité |
| ⚖️ Comparaison Tarif/CRU | Tous | Analyse tarif vs coût réel |
| 🔍 Charges Détaillées | Tous | Détail ligne par ligne |
| 📈 Dashboard | Tous | Vue synthétique graphique |
| 📉 Évolution | Tous | Tendance sur plusieurs années |
| 🏥 Comparaison Hôpitaux | Superuser uniquement | Benchmarking inter-hôpitaux |
| 📊 Comparaison CRU/Tarifs inter | Superuser uniquement | CRU comparé entre hôpitaux |

---

## 3. Lancer le calcul analytique

> **Prérequis :** La saisie du mois (charges, clés de répartition, produits, activités) doit être complète.

1. Cliquer sur l'onglet **🧮 Lancer Calcul**.
2. Vérifier le résumé de la saisie affiché à l'écran.
3. Cliquer sur le bouton **🚀 Lancer le Calcul Analytique**.
4. Attendre la fin du traitement (quelques secondes).
5. Un message de confirmation s'affiche en cas de succès.

**Le calcul exécute les étapes suivantes :**
- Répartition primaire (charges directes)
- Répartition secondaire 1 (déversement NT_UO)
- Répartition secondaire 2
- Calcul des coûts de revient unitaires

> **À noter :** Le calcul peut être relancé autant de fois que nécessaire. Chaque lancement écrase les résultats précédents. Cela est utile après une correction de saisie.

---

## 4. Résultats par Centre de Coût

Cet onglet présente le **tableau analytique principal** : un résumé financier pour chaque centre de coût.

### 4.1 Colonnes du tableau

| Colonne | Description |
|---------|-------------|
| **Code** | Code du centre de coût |
| **Centre de Coût** | Nom du centre |
| **Type** | NT_UO, NT_TF, CT_MT ou CT_CL |
| **Charges Directes** | Charges directement affectées au centre |
| **Charges Indirectes** | Charges reçues par déversement depuis les centres NT_UO |
| **Charges Totales** | Total = Directes + Indirectes |
| **Produits** | Recettes du centre (pour centres tarifaires) |
| **Résultat** | Produits − Charges Totales |

### 4.2 Lecture du tableau

- Un **résultat positif** (vert) signifie que le centre génère plus de recettes qu'il ne consomme de charges.
- Un **résultat négatif** (rouge) indique un déficit sur ce centre.
- Les centres NT_UO and NT_TF n'ont généralement pas de produits — leur résultat est négatif par nature.

---

## 5. Résultats par Centre de Responsabilité

Ce tableau **consolide** les résultats par centre de responsabilité (regroupement de plusieurs centres de coûts).

### 5.1 Colonnes du tableau

| Colonne | Description |
|---------|-------------|
| **Code** | Code du centre de responsabilité |
| **Centre de Responsabilité** | Nom |
| **Nb Centres** | Nombre de centres de coûts inclus |
| **Charges Directes** | Total des charges directes |
| **Charges Indirectes** | Total des charges indirectes |
| **Charges Totales** | Somme totale |
| **Produits** | Total des recettes |
| **Résultat** | Produits − Charges Totales |

---

## 6. Comparaison Tarif vs Coût de Revient Unitaire

Cet onglet est destiné aux **centres tarifaires** (CT_MT et CT_CL). Il compare le tarif pratiqué avec le coût réel de production d'une unité de soin.

### 6.1 Définitions

| Terme | Définition |
|-------|-----------|
| **Coût de Revient Unitaire (CRU)** | Charges Totales ÷ Volume d'activités |
| **Tarif** | Prix facturé aux patients ou à l'assurance |
| **Écart (Tarif − CRU)** | Positif = le tarif couvre les coûts ; Négatif = le tarif est insuffisant |

### 6.2 Colonnes du tableau

| Colonne | Description |
|---------|-------------|
| **Centre de Coût** | Nom du centre tarifaire |
| **Charges totales** | Coût total supporté par le centre |
| **Volume d'activités** | Nombre d'actes/journées saisis |
| **Unité d'Œuvre** | Nature de l'activité (acte, journée...) |
| **Coût de Revient Unitaire** | CRU calculé |
| **Tarif** | Tarif configuré |
| **Écart** | Tarif − CRU |

### 6.3 Interprétation

- **Écart positif et grand** : le tarif est très au-dessus du coût réel — opportunité de révision tarifaire à la baisse ou reflet d'une bonne performance.
- **Écart négatif** : le tarif ne couvre pas les coûts — situation déficitaire — action corrective nécessaire.

---

## 7. Charges Détaillées

L'onglet **🔍 Charges Détaillées** permet d'afficher le détail ligne par ligne des charges, filtrables par période, centre et compte.

Utile pour **contrôler** ou **auditer** les imputations.

---

## 8. Dashboard

L'onglet **📈 Dashboard** présente une **vue synthétique visuelle** des principaux indicateurs :

- Total Charges vs Total Produits
- Résultat global
- Répartition des charges par type de centre
- Centres les plus déficitaires / excédentaires

---

## 9. Évolution sur plusieurs années

L'onglet **📉 Évolution** permet de visualiser la **tendance** des indicateurs clés sur plusieurs exercices.

Sélectionner les années à comparer dans les filtres disponibles.

---

## 10. Comparaison Inter-Hôpitaux (Superuser)

> **Accès réservé au compte superuser.**

### 10.1 Onglet Comparaison Hôpitaux

Permet de comparer les résultats financiers de plusieurs hôpitaux sur une même période.

**Étapes :**
1. Sélectionner l'**Année**.
2. Choisir l'**Indicateur principal** : Résultat / Charges / Produits / Marge (%).
3. Maintenir **Ctrl** (ou **Cmd** sur Mac) et cliquer pour sélectionner plusieurs hôpitaux.
4. Cocher **Hôpitaux actifs seulement** si nécessaire.
5. Cliquer sur **Actualiser**.

**Indicateurs synthétiques :**

| KPI | Description |
|-----|-------------|
| Hôpitaux comparés | Nombre d'hôpitaux dans la sélection |
| Résultat total | Somme des résultats de tous les hôpitaux sélectionnés |
| Moyenne résultat | Résultat moyen par hôpital |
| Écart max/min | Différence entre le meilleur et le moins bon résultat |
| Alertes | Nombre d'alertes détectées |

**Top et Flop :** Le tableau affiche automatiquement les hôpitaux les mieux et les moins bien classés selon l'indicateur choisi.

**Tri des colonnes :** Cliquer sur l'en-tête d'une colonne pour trier le tableau.

**Pagination :** Utiliser les boutons Précédent/Suivant et ajuster le nombre de lignes par page.

### 10.2 Onglet Comparaison CRU/Tarifs inter-hôpitaux

Compare les coûts de revient unitaires et tarifs des prestations entre hôpitaux — utile pour détecter des anomalies tarifaires ou des inefficiences.

---

## 11. Exports Excel et PDF

Chaque tableau de résultats dispose de boutons d'export.

### 11.1 Export Excel

1. Cliquer sur **📥 Export Excel**.
2. Un fichier `.xlsx` est téléchargé automatiquement.
3. Le fichier contient les données du tableau avec mise en forme.

**Tableaux exportables en Excel :**
- Résultats par Centre de Coût
- Résultats par Centre de Responsabilité
- Comparaison Tarif/CRU
- Comparaison Inter-Hôpitaux

### 11.2 Export PDF

1. Cliquer sur **🧾 Export PDF**.
2. Un fichier `.pdf` est téléchargé automatiquement.
3. Le PDF contient le logo et les informations de l'hôpital, la date de génération, et le tableau formaté.

**Tableaux exportables en PDF :**
- Résultats par Centre de Coût
- Résultats par Centre de Responsabilité
- Comparaison Tarif/CRU
- Comparaison Inter-Hôpitaux

### 11.3 Bonnes pratiques pour les exports

- Toujours s'assurer que le calcul analytique a été **lancé** avant d'exporter.
- Vérifier que l'**hôpital** et l'**exercice** corrects sont sélectionnés avant l'export.
- Les exports reflètent les données telles qu'elles sont affichées à l'écran (filtres appliqués).

---

## 12. Lecture et interprétation des résultats

### 12.1 Résultat global

```
Résultat = Total Produits − Total Charges Totales
```

- **Résultat > 0** : L'hôpital génère plus de recettes qu'il ne consomme → excédent.
- **Résultat < 0** : Les charges dépassent les recettes → déficit — action corrective nécessaire.

### 12.2 Coût de Revient Unitaire

```
CRU = Charges Totales du centre ÷ Volume d'activités
```

Le CRU exprime **le coût pour produire une unité de soin** (ex. : 1 acte de laboratoire, 1 journée d'hospitalisation).

### 12.3 Alertes fréquentes

| Alerte | Cause probable | Action |
|--------|---------------|--------|
| CRU très supérieur au tarif | Sous-activité ou charges élevées | Réviser les charges ou augmenter l'activité |
| Résultat très négatif | Charges excessives ou recettes insuffisantes | Analyser les charges détaillées |
| Centre sans activité | Volume d'activité non saisi | Compléter la saisie des activités |
| Charges indirectes très élevées | Clés de répartition déséquilibrées | Revoir les clés de répartition |

---

*Document interne — CASH v1.0 — Confidentiel*
