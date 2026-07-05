from celery.schedules import crontab
from pathlib import Path
import os, environ


# Envrionment Variables

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
else:
    print(f"CRITICAL: .env file not found at {env_file}")


SECRET_KEY = env('DJ_SECRET_KEY')
DEBUG = env('DJ_DEBUG')
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.8.188']
ALLOWED_HOSTS = env.list("DJ_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SUPABASE_URL = env('SUPABASE_URL')
JWKS_URL = env('JWKS_URL')
DJ_ENGINE = env('DJ_ENGINE')
DJ_HOST = env('DJ_HOST')
DJ_NAME = env('DJ_NAME')
DJ_USER = env('DJ_USER')
DJ_PORT = env('DJ_PORT')
DJ_PASSWORD = env('DJ_PASSWORD')


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "drf_api_logger",
    "apps.core",
    "apps.gems",
    "apps.jobs",
]

MIDDLEWARE = [
    "drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


#Databasehttps://docs.djangoproject.com/en/6.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': DJ_ENGINE,
        'HOST': DJ_HOST,
        'NAME': DJ_NAME,
        'USER': DJ_USER,
        'PORT': DJ_PORT,
        'PASSWORD': DJ_PASSWORD,
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    
    # 1. Keep only this authentication class list
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.core.authentication.supabase_auth.SupabaseAuth',
    ],
    
    # 2. Set this to IsAuthenticated if you want your endpoints protected by default
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # 3. Pagination settings
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.global_pagination.StandardResultsSetPagination',
}

SPECTACULAR_SETTINGS = {
    "TITLE": "GemJob API",
    "DESCRIPTION": "API for Job Market and Gem Market",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "ENUM_NAME_OVERRIDES": {
        "JobStatusEnum": "apps.jobs.models.Job.JobStatus", 
        "GemStatusEnum": "apps.gems.models.GemListing.GemStatus",
    },
}

CELERY_BEAT_SCHEDULE = {
    'daily-log-cleanup': {
        'task': 'apps.core.management.commands.tasks.cleanup_api_logs',
        'schedule': crontab(hour=0, minute=0), # Midnight every day
        'args': (7,), # Keep only 7 days of logs
    },
}

# API logger implementation

DRF_API_LOGGER_DATABASE = True
DRF_API_LOGGER_EXCLUDE_KEYS = ['password']
DRF_API_LOGGER_SKIP_URL_NAME = ['health-check', 'prometheus-metrics']
DRF_API_LOGGER_SKIP_NAMESPACE = ['admin']
DRF_API_LOGGER_MAX_REQUEST_BODY_SIZE = 1024
DRF_API_LOGGER_ALL_REQUEST_HEADERS = True
DRF_API_LOGGER_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
