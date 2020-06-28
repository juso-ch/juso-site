"""
Django settings for juso project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django_su',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    "sekizai",
    "admin_ordering",
    "feincms3",
    "feincms3_sites",
    "content_editor",
    "feincms3_meta",
    "ckeditor",
    "imagefield",
    "taggit",
    "juso",
    "juso.sections.apps.SectionsConfig",
    "juso.blog.apps.BlogConfig",
    "juso.pages.apps.PagesConfig",
    "juso.events.apps.EventsConfig",
    "juso.people.apps.PeopleConfig",
    "juso.forms.apps.FormsConfig",
    "juso.glossary.apps.GlossaryConfig",
    "juso.webpush.apps.WebpushConfig",
    "juso.link_collections.apps.LinkCollectionsConfig",
    "django_celery_results",
]

MIDDLEWARE = [
    'feincms3_sites.middleware.site_middleware',
    'feincms3_sites.middleware.default_language_middleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'feincms3.apps.apps_middleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'juso.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
            ],
            'builtins': [
                'feincms3.templatetags.feincms3',
            ]
        },
    },
]

WSGI_APPLICATION = 'juso.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = [
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

# Configure django-ckeditor
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "format_tags": "h1;h2;h3;p;pre",
        "toolbar_Custom": [[
            "Format", "RemoveFormat", "-",
            "Bold", "Italic", "Subscript", "Superscript", "-",
            "NumberedList", "BulletedList", "-",
            "Anchor", "Link", "Unlink", "-",
            "HorizontalRule", "SpecialChar", "-",
            "Source",
        ]],
    },
}
CKEDITOR_CONFIGS["richtext-plugin"] = CKEDITOR_CONFIGS["default"]

TEAM_TEMPLATE_CHOICES = (
    ('teams/default.html', _("default")),
)

EVENT_TEMPLATE_CHOICES = (
    ('events/plugins/default.html', _("default")),
)

BLOG_TEMPLATE_CHOICES = (
    ('blog/plugins/default.html', _("default")),
    ('blog/plugins/simple_list.html', _("list")),
)


LANGUAGES = (
    ("de", _("German")),
    ("fr", _("French")),
    ("it", _("Italian")),
)
LANGUAGE_CODE = 'de'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_su.backends.SuBackend',
]

AJAX_LOOKUP_CHANNELS = {'django_su':  dict(
    model='auth.user', search_field='username'
)}

SU_LOGIN_REDIRECT_URL = "/admin/"
SU_LOGOUT_REDIRECT_URL = "/admin/"


def superuser_callback(user):
    return user.is_superuser

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEBUG = int(os.environ.get("DEBUG", default=0))

LANGUAGE_COOKIE_SECURE = not DEBUG
LANGUAGE_COOKIE_SAMESITE = 'strict'

CSRF_COOKIE_SAMESITE = 'strict'
CSRF_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SECURE = not DEBUG
#SESSION_COOKIE_NAME = '__Secure-sessionid'
SESSION_COOKIE_SAMESITE = 'Lax'

SU_LOGIN_CALLBACK = "juso.settings.superuser_callback"

NOMINATIM_USER_AGENT = 'juso-site'

FONTAWESOME_5_ICON_CLASS = 'semantic_ui'

SECRET_KEY = os.environ.get("SECRET_KEY", 'changeme')


ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


DEFAULT_COLOR = "#eb141f"


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MAPS_URL = "https://www.google.com/maps/dir/My+Location/{location.lat},{location.lng}"


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache:11211',
    }
}

EMAIL_HOST = 'smtp'
EMAIL_PORT = 25

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", 'webmaster@localhost')
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", 'root@localhost')


CELERY_BROKER_URL = "redis://redis:6379"

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

VAPID_EMAIL = os.environ.get('VAPID_EMAIL', '')

VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', '')
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', '')
