import logging
import os
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = ROOT_DIR / "core_apps"

# This env variable is placed in the Dockerfile
AM_I_IN_DOCKER_CONTAINER = env.bool("AM_I_IN_DOCKER_CONTAINER", False)

# When running in a docker container, we set the env variables in the docker-compose.yml file
# so we don't need to do read_env, but if we want to run the project locally outside of docker
# we need to read the env variables manually
if not AM_I_IN_DOCKER_CONTAINER:
    # When outside of a docker container always load local envs
    django_env_local = os.path.join(ROOT_DIR, ".envs", ".local", ".django")
    postgres_env_local = os.path.join(ROOT_DIR, ".envs", ".local", ".postgres")

    env.read_env(django_env_local)
    env.read_env(postgres_env_local)


DEBUG = env.bool("DJANGO_DEBUG", False)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "core_apps.blogs": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "core_apps.common": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "core_apps.users": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework.authtoken",
]
THIRD_PARTY_APPS = [
    "rest_framework",
]

LOCAL_APPS = ["core_apps.blogs", "core_apps.users", "core_apps.common"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "production_ready_blog_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {"default": env.db()}

# In docker the host is set as postgres (name of the container), that fails locally
# Important!!: If you have started a postgres connection before in your computer
# you need to create a new user and a database with the same values as in the .envs/.local/.postgres file
if not AM_I_IN_DOCKER_CONTAINER:
    DATABASES["default"]["HOST"] = "127.0.0.1"


WSGI_APPLICATION = "production_ready_blog_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

ADMIN_URL = "admin/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/staticfiles/"

# python manage.py collectstatic will collect all static files and put them here
# this was it is more efficent for nginx to serve them
STATIC_ROOT = str(ROOT_DIR / "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# They use the same host for redis, but point to different DBs
CELERY_BROKER_URL = env("CELERY_BROKER")
REDIS_CACHE_URL = env("REDIS_CACHE_URL")

# In docker the celery broker host needs to be "redis" which fails locally
if not AM_I_IN_DOCKER_CONTAINER:
    CELERY_BROKER_URL = CELERY_BROKER_URL.replace("//redis", "//127.0.0.1")
    REDIS_CACHE_URL = REDIS_CACHE_URL.replace("//redis", "//127.0.0.1")


# Redis cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# Using Redis as broker and result backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# List of content types that the worker can deserialize
CELERY_ACCEPT_CONTENT = ["json"]
# Serialization for takss before sending them to the broker
CELERY_TASK_SERIALIZER = "json"
# Serialization format for task results
CELERY_RESULT_SERIALIZER = "json"
# maximum number of retries that should be attempted when storing task results in the result backend.
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# Celery will send an event every time a task is sent (Can be caught and used for monitoring)
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_TIMEZONE = TIME_ZONE

# Probably we only want sentry on in production
SENTRY_DSN = env.str("SENTRY_DSN", None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Log in sentry logs from info level and above
        integrations=[LoggingIntegration(level=logging.INFO, event_level=logging.INFO)],
        enable_tracing=True,
        # Track which user is sending requests
        traces_sample_rate=1.0,
        # Percentage of requests to be profiled (see how code is performing)
        profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE", 0.1),
    )
