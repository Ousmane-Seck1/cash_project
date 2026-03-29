# Guide Utilisateur - Referentiel par Niveau (N1/N2/N3)

## 1. Objectif
Cette fonctionnalite permet de copier un referentiel de configuration entre hopitaux du meme niveau (N1, N2, N3), tout en preservant par defaut les parametres locaux des centres (type, unite d'oeuvre, tarif).

## 2. Prerequis
- Vous devez etre superuser pour lancer les operations de copie par niveau.
- Un hopital de reference doit exister pour chaque niveau.

## 3. Endpoints utiles

### 3.1 Precheck annuel
GET /api/exercices/workflow_annuel_precheck/?hopital=<ID>

Retourne:
- ready (true/false)
- checks (liste des verifications)
- next_steps (etapes conseillees)

### 3.2 Apercu avant copie (sans impact)
POST /api/hopitaux/<ID_CIBLE>/copier_referentiel_niveau/
Body JSON:
{
  "preview_only": true
}

Retourne un "diff" avec les elements a ajouter et deja presents.

### 3.3 Copie standard par niveau
POST /api/hopitaux/<ID_CIBLE>/copier_referentiel_niveau/
Body JSON:
{}

- Copie depuis l'hopital de reference du meme niveau.
- Ne force pas les parametres locaux des centres.

### 3.4 Copie forcee (ecrase les parametres locaux des centres)
POST /api/hopitaux/<ID_CIBLE>/copier_referentiel_niveau/
Body JSON:
{
  "force": true,
  "confirmation_code": "CONFIRMER"
}

Important:
- Sans confirmation_code=CONFIRMER, l'operation est refusee.

### 3.5 Controle qualite
GET /api/hopitaux/controle_qualite_donnees/

Retourne les anomalies (fonctions absentes, comptes absents, UO manquante, tarif manquant, exercice actif manquant).

### 3.6 Alertes systeme
GET /api/hopitaux/alertes_systeme/

Retourne:
- anomalies qualite
- references de niveau manquantes
- compteur d'audits du jour

## 4. Bonnes pratiques
1. Toujours lancer preview_only avant une copie.
2. Utiliser force=true uniquement si vous voulez aligner strictement les centres.
3. Verifier controle_qualite_donnees apres toute copie.
4. Verifier alertes_systeme chaque jour en exploitation.

## 5. Parametrage actuel (initial)
- N1 reference: CHRT
- N2 reference: CHRF
- N3 reference: CHRK
