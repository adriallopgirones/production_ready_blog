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

# TODO: Do we need CORS, I can't think of a reason why we would in the context of
# a backend for a smartphone app
# CORS it's a security feature used by webrowers to prevent cross site scripting
# for example www.google.com can't make a request to www.facebook.com
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
