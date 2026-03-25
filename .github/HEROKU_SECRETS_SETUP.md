# Configuration des Secrets GitHub pour Déploiement Heroku

## 🔐 Vue d'ensemble

Ce guide explique comment configurer les secrets GitHub pour déployer l'application sur Heroku avec CI/CD automatisé.

## 📋 Prérequis

- Compte GitHub (✅ Vous l'avez déjà)
- Compte Heroku (créer sur https://heroku.com)
- Accès SSH/terminal local
- Git installé

## 🚀 Étape 1 : Créer compte Heroku et app

### 1. Signup Heroku
- Aller sur https://signup.heroku.com/
- Créer un compte (email + password)
- Confirmer l'email

### 2. Créer l'application Heroku

**Via le Dashboard Heroku :**
```
https://dashboard.heroku.com → New → Create new app
App name: cash-project-senegal (ou votre choix)
Region: Select (Europe si possible pour latence basse)
```

**Ou via terminal :**
```bash
# Installer Heroku CLI
npm install -g heroku
# ou
choco install heroku-cli  # Windows

# Login
heroku login

# Créer l'app
heroku create cash-project-senegal

# Ajouter PostgreSQL (gratuit avec hobby-dev)
heroku addons:create heroku-postgresql:hobby-dev -a cash-project-senegal
```

### 3. Obtenir votre HEROKU_API_KEY

1. Aller sur https://dashboard.heroku.com/account/applications/authorizations
2. Cliquer sur **Create authorization**
3. Donner une description : "GitHub Actions CI/CD"
4. Copier la clé générée (elle n'apparaîtra qu'une fois)
5. Ajouter dans GitHub Secrets

## 🔑 Étape 2 : Ajouter les Secrets GitHub

### Accès aux Secrets

1. Aller sur votre repo GitHub :
   ```
   https://github.com/Ousmane-Seck1/cash_project
   ```

2. Cliquer sur **Settings** (onglet en haut à droite)

3. Dans le menu gauche : **Secrets and variables** → **Actions**

4. Cliquer sur **New repository secret**

### Ajouter chaque Secret

| # | Secret Name | Valeur | Exemple |
|---|-------------|--------|---------|
| 1 | `HEROKU_API_KEY` | Votre clé API Heroku | `abc123def456...` |
| 2 | `HEROKU_APP_NAME` | Nom de l'app Heroku | `cash-project-senegal` |
| 3 | `HEROKU_EMAIL` | Email compte Heroku | `you@example.com` |
| 4 | `SECRET_KEY` | Clé Django sécurisée | `a4f7$kj@9x#mpl2$k` |
| 5 | `ALLOWED_HOSTS` | Domaines autorisés | `cash-project-senegal.herokuapp.com` |
| 6 | `DB_ENGINE` | Django DB backend | `django.db.backends.postgresql` |
| 7 | `DB_NAME` | Nom base données | `cash_db` |
| 8 | `DB_USER` | User BD | `cash_user` |
| 9 | `DB_PASSWORD` | Password BD | `secure_password_here` |
| 10 | `DB_HOST` | Host PostgreSQL | (Heroku le configure via DATABASE_URL) |
| 11 | `DB_PORT` | Port PostgreSQL | `5432` |

### Pour chaque secret, faire ceci :

```
1. Name: [Nom du secret]
2. Secret: [Valeur]
3. Cliquer "Add secret"
```

### Exemple détaillé pour HEROKU_API_KEY :

```
Name: HEROKU_API_KEY
Secret: 12ab34cd-56ef-78gh-90ij-klmnopqrst12
```

(Remplacer par votre vraie clé)

## ⚙️ Étape 3 : Créer les Environnements

1. Dans GitHub : **Settings** → **Environments**
2. Cliquer **New environment**
3. Créer `staging` :
   ```
   Name: staging
   Ajouter les mêmes secrets que ci-dessus
   ```
4. Créer `production` :
   ```
   Name: production
   Ajouter les mêmes secrets
   ⚠️ Optionnel : Cocher "Required reviewers" pour approver avant déployer
   ```

## 🔄 Étape 4 : Tester le Déploiement

### Via GitHub Actions (Recommandé)

1. Aller sur votre repo GitHub
2. Onglet **Actions**
3. Cliquer sur le workflow **"Deployment (Manual)"**
4. Cliquer **"Run workflow"**
5. Sélectionner l'environnement : `staging`
6. Cliquer **"Run workflow"**
7. Attendre la fin (5-10 minutes)
8. Vérifier la sortie des logs

### Vérifier que le déploiement a réussi

```bash
# Voir les apps Heroku
heroku apps

# Voir les logs de l'app
heroku logs --tail -a cash-project-senegal

# Vérifier la BD PostgreSQL
heroku pg:info -a cash-project-senegal
heroku psql -a cash-project-senegal  # Connexion BD
```

### Accéder à l'app en production

```
https://cash-project-senegal.herokuapp.com
```

## 🐛 Dépannage

### Erreur : "HEROKU_API_KEY not found"
- ✅ Solution : Vérifier que le secret est bien ajouté dans GitHub

### Erreur : "DATABASE_URL not configured"
- ✅ Solution : S'assurer que le PostgreSQL addon est bien créé :
  ```bash
  heroku addons -a cash-project-senegal
  ```

### L'app Heroku démarre mais erreur 500
```bash
# Voir les erreurs
heroku logs --tail -a cash-project-senegal

# Vérifier les migrations
heroku run python manage.py migrate -a cash-project-senegal

# Créer un superuser
heroku run python manage.py createsuperuser -a cash-project-senegal
```

### PostGres ne se connecte pas
```bash
# Vérifier que DATABASE_URL existe
heroku config -a cash-project-senegal

# Si absent, ajouter la BD
heroku addons:create heroku-postgresql:hobby-dev -a cash-project-senegal
```

## 📝 Checklist Finale

Avant de déployer en production :

- [ ] Tous les secrets GitHub sont configurés
- [ ] Environnements `staging` et `production` créés
- [ ] Heroku app créée avec PostgreSQL
- [ ] Tests passent localement (`python manage.py test`)
- [ ] Aucun secret hardcodé dans le code
- [ ] CSRF_COOKIE_SECURE = True en production
- [ ] DEBUG = False en production
- [ ] Domaine configuré dans ALLOWED_HOSTS
- [ ] Email SMTP configuré (optionnel pour notifications)
- [ ] Logs activés et accessibles
- [ ] Backup BD programmé (optionnel)

## 🎯 Workflow de Déploiement Recommandé

```
1. Développement local
   ↓
2. Push vers GitHub (branche develop ou feature)
   ↓
3. CI/CD tests automatiques (tests.yml + quality.yml)
   ↓
4. Si tests ✅ → Merge vers main
   ↓
5. Workflow deploy.yml se déclenche manuellement
   ↓
6. Déploiement à staging (tests finaux)
   ↓
7. Approvation → Merge vers production
   ↓
8. App en production sur Heroku
```

## 🔗 Ressources Utiles

- [Heroku Django Guide](https://devcenter.heroku.com/articles/deploying-python)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Heroku PostgreSQL](https://devcenter.heroku.com/articles/heroku-postgresql)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

**Support :** En cas de problème, vérifier les logs :
```bash
# Logs GitHub Actions
GitHub > Actions > Workflow run > Logs

# Logs Heroku
heroku logs --tail -a cash-project-senegal
```
