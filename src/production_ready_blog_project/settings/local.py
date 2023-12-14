from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
# Ran python -c "import secrets; print(secrets.token_urlsafe(38))" to obtain a new secret key
SECRET_KEY = (
    env(  # noqa
        "DJANGO_SECRET_KEY",
        default="DvMUU3Taijp4oVLVSOVqvQ72dEkRw2hTe80Av6vYu3mG4dFxmo0",
    ),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# CORS it's a security feature used by webrowers to prevent cross site scripting
# for example www.google.com can't make a request to www.facebook.com


# When running on nginx the origin is 8000 and we need to add it here
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
