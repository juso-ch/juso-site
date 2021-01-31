"""
Django settings for juso project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
    "content_editor",

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _
from html_sanitizer.sanitizer import (
    bold_span_to_strong,
    italic_span_to_em,
    tag_replacer,
    target_blank_noopener,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "django_su",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "reversion",
    "sekizai",
    "admin_ordering",
    "feincms3",
    "feincms3_sites",
    "feincms3_meta",
    "ckeditor",
    "imagefield",
    "taggit",
    "juso",
    "content_editor",
    "flat_json_widget",
    "juso.sections.apps.SectionsConfig",
    "juso.blog.apps.BlogConfig",
    "juso.pages.apps.PagesConfig",
    "juso.events.apps.EventsConfig",
    "juso.people.apps.PeopleConfig",
    "juso.forms.apps.FormsConfig",
    "juso.glossary.apps.GlossaryConfig",
    "juso.webpush.apps.WebpushConfig",
    "juso.testimonials.apps.TestimonialsConfig",
    "juso.link_collections.apps.LinkCollectionsConfig",
    "django_celery_results",
]

MIDDLEWARE = [
    "feincms3_sites.middleware.site_middleware",
    "feincms3_sites.middleware.redirect_to_site_middleware",
    "feincms3_sites.middleware.default_language_middleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "feincms3.apps.apps_middleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "juso.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
            ],
            "builtins": [
                "feincms3.templatetags.feincms3",
            ],
            "loaders": [
                (
                    "juso.template.SiteTemplateLoader",
                    ["custom/templates"],
                    ["base.html"],
                ),
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

WSGI_APPLICATION = "juso.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

TIME_ZONE = "Europe/Zurich"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = ["custom/static"]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Configure django-ckeditor
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar":
        "Custom",
        "format_tags":
        "h1;h2;h3;h4;p;pre",
        "toolbar_Custom": [[
            "Format",
            "RemoveFormat",
            "-",
            "Undo",
            "Redo",
            "-",
            "Bold",
            "Italic",
            "Strike",
            "Subscript",
            "Superscript",
            "-",
            "NumberedList",
            "BulletedList",
            "Table",
            "Blockquote",
            "-",
            "Anchor",
            "Link",
            "Unlink",
            "-",
            "HorizontalRule",
            "SpecialChar",
            "-",
            "ShowBlocks",
            "Source",
        ]],
    },
}
CKEDITOR_CONFIGS["richtext-plugin"] = CKEDITOR_CONFIGS["default"]

TEAM_TEMPLATE_CHOICES = (("teams/default.html", _("default")), )

EVENT_TEMPLATE_CHOICES = (("events/plugins/default.html", _("default")), )

BLOG_TEMPLATE_CHOICES = (
    ("blog/plugins/default.html", _("default")),
    ("blog/plugins/simple_list.html", _("list")),
)

LANGUAGES = (
    ("de", _("German")),
    ("fr", _("French")),
    ("it", _("Italian")),
)
LANGUAGE_CODE = "de"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "django_su.backends.SuBackend",
]

AJAX_LOOKUP_CHANNELS = {
    "django_su": dict(model="auth.user", search_field="username")
}

SU_LOGIN_REDIRECT_URL = "/admin/"
SU_LOGOUT_REDIRECT_URL = "/admin/"


def superuser_callback(user):
    return user.is_superuser


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
DEBUG = int(os.environ.get("DEBUG", default=0))

if DEBUG:
    MIDDLEWARE.remove("feincms3_sites.middleware.redirect_to_site_middleware")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INSTALLED_APPS.append("debug_toolbar")

LANGUAGE_COOKIE_SECURE = not DEBUG
LANGUAGE_COOKIE_SAMESITE = "strict"

CSRF_COOKIE_SAMESITE = "strict"
CSRF_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SECURE = not DEBUG
# SESSION_COOKIE_NAME = '__Secure-sessionid'
SESSION_COOKIE_SAMESITE = "Lax"

SU_LOGIN_CALLBACK = "juso.settings.superuser_callback"

NOMINATIM_USER_AGENT = "juso-site"

FONTAWESOME_5_ICON_CLASS = "semantic_ui"

SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("POSTGRES_DB",
                               os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

DEFAULT_COLOR = "#eb141f"

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"), )

MAPS_URL = "https://www.google.com/maps/dir/My+Location/{location.lat},{location.lng}"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "cache:11211",
    }
}

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL",
                                    "webmaster@localhost")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "root@localhost")

EMAIL_HOST = os.environ.get("SMTP_HOST", "smtp")
EMAIL_PORT = int(os.environ.get("SMTP_PORT", "25"))

EMAIL_USE_TLS = int(os.environ.get("SMTP_TLS", "0"))
EMAIL_USE_SSL = int(os.environ.get("SMTP_SSL", "0"))

EMAIL_HOST_USER = os.environ.get("SMTP_USER", "user")
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", "pw")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL",
                                    "webmaster@localhost")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "root@localhost")

CELERY_BROKER_URL = "redis://redis:6379"

CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"

VAPID_EMAIL = os.environ.get("VAPID_EMAIL", "")

VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_PUBLIC_KEY = os.environ.get("VAPID_PUBLIC_KEY", "")


def sanitize_href(url):
    return url


def is_mergeable(e1, e2):
    table_tags = ["tr", "td", "th"]
    return e1.tag not in table_tags


HTML_SANITIZERS = {
    "default": {
        "tags": {
            "a",
            "h1",
            "h2",
            "h3",
            "h4",
            "strong",
            "em",
            "p",
            "ul",
            "ol",
            "li",
            "br",
            "sub",
            "sup",
            "hr",
            "table",
            "td",
            "tr",
            "th",
            "tbody",
            "thead",
            "caption",
        },
        "attributes": {
            "a": ("href", "name", "target", "title", "id", "rel", "class"),
            "table": ("summary"),
        },
        "empty": {"hr", "a", "br"},
        "separate": {"a", "p", "li"},
        "whitespace": {"br"},
        "keep_typographic_whitespace":
        False,
        "add_nofollow":
        False,
        "autolink":
        False,
        "sanitize_href":
        sanitize_href,
        "element_preprocessors": [
            bold_span_to_strong,
            italic_span_to_em,
            tag_replacer("b", "strong"),
            tag_replacer("i", "em"),
            tag_replacer("form", "p"),
            target_blank_noopener,
        ],
        "element_postprocessors": [],
        "is_mergeable":
        is_mergeable,
    }
}

MAILTRAIN_URL = os.environ.get("MAILTRAIN_URL", "")
MAILTRAIN_TOKEN = os.environ.get("MAILTRAIN_TOKEN", "")


def toolbar_callback(*args):
    return False


INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "juso.settings.toolbar_callback",
}

JAZZMIN_SETTINGS = {
    # title of the window
    "site_title":
    _("JUSO"),
    # Title on the brand, and the login screen (19 chars max)
    "site_header":
    _("JUSO"),
    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo":
    "logo.png",
    # Welcome text on the login screen
    "welcome_sign":
    _("JUSO Admin"),
    # Copyright on the footer
    "copyright":
    "JUSO Schweiz",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model":
    "blog.Article",
    # Field name on user model that contains avatar image
    "user_avatar":
    None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
    # Url that gets reversed (Permissions can be added)
        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["auth.view_user"]
        },
    # external url that opens in a new window (Permissions can be added)
    # model admin to link to (Permissions checked against model)
        {
            "model": "blog.Article"
        },
        {
            "model": "pages.Page"
        },
    # App with dropdown menu to all its models pages (Permissions checked against models)
        {
            "app": "events"
        },
        {
            "name": "Support",
            "url": "https://github.com/juso-ch/juso-site/wiki",
            "icon": "fas fa-question-circle",
        },
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar":
    True,
    # Whether to aut expand the menu
    "navigation_expanded":
    True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps":
    ["webpush", "testimonials", "taggit", "django_celery_results"],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "pages",
        "blog",
        "events",
        "people",
        "forms",
        "link_collections",
        "people.Person",
        "people.Team",
    ],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"],
        }]
    },
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "blog.Article": "fas fa-newspaper",
        "pages.Page": "fas fa-file",
        "blog.NameSpace": "fas fa-tags",
        "blog.WPImport": "fab fa-wordpress",
        "events.Event": "fas fa-calendar",
        "events.Location": "fas fa-map-marker-alt",
        "people.CandidateList": "fas fa-vote-yea",
        "people.Person": "fas fa-user",
        "people.Team": "fas fa-users",
        "forms.Form": "fab fa-wpforms",
        "forms.MailchimpConnection": "fab fa-mailchimp",
        "forms.FormEntry": "fas fa-grip-lines",
        "forms.Webhook": "fas fa-paper-plane",
        "link_collections.Collection": "fas fa-list",
        "glossary.Entry": "fas fa-book-open",
        "sections.Category": "fas fa-tags",
        "feincms3_sites.Site": "fas fa-globe",
        "sections.Section": "fas fa-sitemap",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents":
    "fas fa-chevron-circle-right",
    "default_icon_children":
    "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active":
    True,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css":
    "admin.css",
    "custom_js":
    None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder":
    False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format":
    "vertical_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
    #        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Add a language dropdown into the admin
    "language_chooser":
    True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-danger navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": "",
    "actions_sticky_top": True,
}

X_FRAME_OPTIONS = "SAMEORIGIN"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
