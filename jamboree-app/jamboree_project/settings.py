# jamboree_project/settings.py

from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configuration de Production ---
# SECRET_KEY, DEBUG et DATABASE_URL seront lus depuis les variables d'environnement de Render
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Le nom d'hôte de votre application sur Render sera automatiquement ajouté.
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# render_external_hostname = config('RENDER_EXTERNAL_HOSTNAME', default=None)
# if render_external_hostname:
#     ALLOWED_HOSTS.append(render_external_hostname)
ALLOWED_HOSTS = ['jamboree-app.onrender.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Important: pour les fichiers statiques
    'django.contrib.staticfiles',
    'cotisations',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Important: juste après SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jamboree_project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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
WSGI_APPLICATION = 'jamboree_project.wsgi.application'

# --- Base de données (configurée pour Render) ---
DATABASES = {
    'default': dj_database_url.config(
        # En local, il cherchera une variable DATABASE_URL dans un fichier .env
        # Sur Render, il utilisera la variable d'environnement DATABASE_URL fournie par le service de BDD.
        default='sqlite:///db.sqlite3', # Une base de secours si DATABASE_URL n'est pas définie
        conn_max_age=600
    )
}

# ... (Auth validators)

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Fichiers Statiques (configurés pour Render avec WhiteNoise) ---
STATIC_URL = 'static/'
# Ce dossier sera créé pour rassembler tous les fichiers statiques avant le déploiement
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'