# CI/CD avec GitHub Actions

Ce projet inclut trois workflows GitHub Actions automatisés :

## 1. Tests (`tests.yml`)
**Déclenché automatiquement** sur chaque push/PR vers `main` ou `develop`

✅ Exécute les tests Django
✅ Teste sur Python 3.10 et 3.11
✅ Teste avec PostgreSQL en service
✅ Lint Python (flake8, black, pylint)
✅ Scan de sécurité (bandit)

**Pour déboguer localement :**
```bash
python manage.py test --verbosity=2
flake8 analytics cash_project
black analytics cash_project
```

## 2. Vérification de Qualité (`quality.yml`)
**Déclenché automatiquement** sur chaque push/PR

✅ Vérifie la configuration Django
✅ Controlle le format du code (Black)
✅ Analyse statique (pylint)
✅ Scan de sécurité complet
✅ Vérification des dépendances vulnérables

## 3. Déploiement (`deploy.yml`)
**Déclenché manuellement** via GitHub > Actions > Workflow Dispatch

⚠️ Nécessite la configuration des secrets GitHub Actions

### Configuration du Déploiement

#### Étape 1 : Configurer les Secrets GitHub

Aller sur : **Settings** > **Secrets and variables** > **Actions**

Ajouter ces secrets (remplacer par les vraies valeurs) :

```
SECRET_KEY              → Clé Django sécurisée (voir .env.example)
ALLOWED_HOSTS           → Domaines autorisés (ex: yourdomain.com)
DB_ENGINE               → django.db.backends.postgresql
DB_NAME                 → Nom de la BD
DB_USER                 → Utilisateur BD
DB_PASSWORD             → Mot de passe BD
DB_HOST                 → IP/Host du serveur BD
DB_PORT                 → Port BD (défaut: 5432)
EMAIL_HOST              → SMTP server (ex: smtp.gmail.com)
EMAIL_PORT              → Port SMTP (ex: 587)
EMAIL_HOST_USER         → Email pour notifications
EMAIL_HOST_PASSWORD     → Mot de passe email
SLACK_WEBHOOK           → (Optionnel) Webhook pour notifications Slack
```

#### Étape 2 : Configurer l'Environnement de Déploiement

Dans **Settings** > **Environments** :

1. Créer un environnement `staging` (pour tests)
2. Créer un environnement `production` (pour prod)
3. Ajouter les secrets requis pour chaque environnement
4. (Optionnel) Configurer les règles d'approbation pour production

#### Étape 3 : Adapter le Processus de Déploiement

Éditer `.github/workflows/deploy.yml` et remplacer la section TODO par votre processus réel :

**Exemple pour un serveur Linux via SSH :**
```yaml
    - name: Deploy via SSH
      run: |
        mkdir -p ~/.ssh
        echo "${{ secrets.DEPLOY_KEY }}" > ~/.ssh/deploy_key
        chmod 600 ~/.ssh/deploy_key
        ssh -i ~/.ssh/deploy_key user@your-server.com \
          'cd /var/www/cash_project && \
           git pull origin main && \
           source venv/bin/activate && \
           pip install -r requirements.txt && \
           python manage.py migrate && \
           python manage.py collectstatic --noinput && \
           systemctl restart cash_project'
```

**Exemple pour Heroku :**
```yaml
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

**Exemple pour AWS EC2 :**
```yaml
    - name: Deploy to AWS
      run: |
        aws s3 sync . s3://your-bucket/cash-project --exclude ".git/*"
        aws ec2-instance-connect send-ssh-public-key \
          --instance-id ${{ secrets.AWS_INSTANCE_ID }} \
          --os-user ubuntu \
          --ssh-public-key.format openssh
```

### Statut des Workflows

Tous les workflows passent doivent retourner **✅ Succès** pour pouvoir merger sur `main`.

Voir le statut : **Code** > **Actions** (sur GitHub)

### Dépannage

**Tests échouent localement mais passent sur CI :**
- Les migrations peuvent être en cache. Nettoyer : `rm db.sqlite3`
- Les variables d'env peuvent être manquantes. Créer : `cp .env.example .env`

**Déploiement échoue :**
1. Vérifier les logs dans GitHub Actions
2. Vérifier que tous les secrets sont configurés
3. Vérifier la connectivité vers le serveur de déploiement

**Ajouter une notification Slack :**
1. Créer un webhook Slack
2. Ajouter le secret `SLACK_WEBHOOK` dans GitHub
3. Les notifications sont déjà incluses dans `deploy.yml`

---

Pour plus d'info : https://docs.github.com/actions
