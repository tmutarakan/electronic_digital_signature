from api.settings.base import *  # подгружаем настройки по умолчанию

DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS += ["debug_toolbar", "django_extensions"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
