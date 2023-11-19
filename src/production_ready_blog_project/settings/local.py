from .base import *  # noqa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
# Ran python -c "import secrets; print(secrets.token_urlsafe(38))" to obtain a new secret key
SECRET_KEY = (
    env(
        "DJANGO_SECRET_KEY",
        default="DvMUU3Taijp4oVLVSOVqvQ72dEkRw2hTe80Av6vYu3mG4dFxmo0",
    ),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TODO: Use CRFS
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
