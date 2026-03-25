"""
Configuration Django pour CASH - Comptabilité Analytique Hospitalière Sénégal
"""


import os
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    # Charger depuis .env.example si .env n'existe pas
    load_dotenv(Path(__file__).resolve().parent.parent / '.env.example')

# ==========  CONFIGURATION DE BASE ==========

BASE_DIR = Path(__file__).resolve().parent.parent
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# ========== SÉCURITÉ ==========

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY or 'insecure' in SECRET_KEY:
    raise ValueError('⚠️  SECRET_KEY non configurée. Copier .env.example en .env et générer une clé sécurisée.')

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

if not DEBUG and not SECRET_KEY.startswith('django-insecure'):
    print('✅ Production mode: DEBUG=False, SECRET_KEY sécurisée')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF & Session Security
is_production = ENVIRONMENT == 'production' or not DEBUG
CSRF_COOKIE_SECURE = is_production
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = is_production
SESSION_COOKIE_HTTPONLY = True

# ========== APPLICATIONS ==========

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    # Local apps
    'analytics.apps.AnalyticsConfig',
]


# ========== MIDDLEWARE ==========

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


# ========== TEMPLATES & URLS ==========

ROOT_URLCONF = 'cash_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Important !
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'cash_project.wsgi.application'


# ========== BASE DE DONNÉES ==========

db_engine = os.getenv('DB_ENGINE', 'sqlite3')

if db_engine == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
        }
    }
elif db_engine in ['postgresql', 'django.db.backends.postgresql']:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    raise ValueError(f'❌ DB_ENGINE inconnu: {db_engine}')


# ========== SESSION & AUTHENTIFICATION ==========
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/accueil/'
LOGOUT_REDIRECT_URL = '/login/'


# ========== VALIDATION DES MOTS DE PASSE ==========
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ========== MESSAGES ==========

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
}


# ========== INTERNATIONALISATION ==========
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Dakar'
USE_I18N = True
USE_TZ = True


# ========== FICHIERS STATIQUES ==========

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ========== DJANGO REST FRAMEWORK ==========

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}


# ========== CORS ==========

cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(',')]

if not DEBUG:
    CORS_ALLOW_CREDENTIALS = True


# ========== LOGGING ==========

LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'django.log'),  # str() pour Windows
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'analytics': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}