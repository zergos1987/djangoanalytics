"""
Django settings for djangoanalytics project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import os

import logging
from custom_script_extensions.djangoanalytics_initialize import initialazie_base_content
from logging.handlers import RotatingFileHandler
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get("SECRET_KEY", config('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", config('DEBUG', default=False, cast=bool))
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", config('ALLOWED_HOSTS')).split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg2',
    'rest_framework',
    'django_filters',
    'rangefilter',
    'crispy_forms',
    'csp',
    'import_export',
    'sslserver',
    'widget_tweaks',
    'apps.accounts',
    'apps.app_zs_admin',
    'apps.app_opensource_dashboards',
    'apps.app_opensource_surveys',
    'apps.app_zs_dashboards',
    'apps.app_zs_examples',
    'apps.database_oracle_sadko',
    'apps.database_sqlite_test',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django_python3_ldap.auth.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

ROOT_URLCONF = 'djangoanalytics.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR  / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'builtins': [
            #     'custom_script_extensions.form_tags'
            # ],
            'libraries': {
                'form_tags': 'custom_script_extensions.form_tags',
                'template_filters': 'custom_script_extensions.template_filters',
            },
        },
    },
]

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

WSGI_APPLICATION = 'djangoanalytics.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_ROUTERS = ['custom_script_extensions.database_router.CheckerRouter']
DATABASE_APPS_MAPPING = {
    'accounts': 'default',
    'app_zs_admin': 'default',
    'app_opensource_dashboards': 'default',
    'app_opensource_surveys': 'default',
    'app_zs_dashboards': 'default',
    'app_zs_examples': 'default',
    'database_oracle_sadko': 'oracle_sadko_db',
    'database_sqlite_test': 'test_remote_db',
}
DATABASES = {
    # [W - setup] ################################
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    },
    # 'oracle_sadko_db': {
    #     'ENGINE': 'django.db.backends.oracle',
    #     'HOST': os.environ.get("Sadko_Host_os", config('Sadko_Host_env')),
    #     'PORT': os.environ.get("Sadko_Port_os", config('Sadko_Port_env')),
    #     'NAME': os.environ.get("Sadko_Database_os", config('Sadko_Database_env')),
    #     'USER': os.environ.get("Sadko_Login_os", config('Sadko_Login_env')),
    #     'PASSWORD': os.environ.get("Sadko_Password_os", config('Sadko_Password_env')),
    # },
    # 'BusinessObjects_sybase_db': {
    #     'ENGINE': 'sqlany_django', # OUTDATE DRIVER = NOT WORKED !
    #     'NAME': os.environ.get("BusinessObjects_Database_os", config('BusinessObjects_Database_env')),
    #     'USER': os.environ.get("BusinessObjects_Login_os", config('BusinessObjects_Login_env')),
    #     'PASSWORD': os.environ.get("BusinessObjects_Password_os", config('BusinessObjects_Password_env')),
    #     'HOST': os.environ.get("BusinessObjects_Host_os", config('BusinessObjects_Host_env')),
    #     'PORT': os.environ.get("BusinessObjects_Port_os", config('BusinessObjects_Port_env')),
    # }
    # '_mssql_db': {
    #     'ENGINE': 'mssql',
    #     'NAME': os.environ.get("_mssql_Database_os", config('_mssql_Database_env')),
    #     'HOST': os.environ.get("_mssql_Host_os", config('_mssql_Host_env')),
    #     'PORT': os.environ.get("_mssql_Port_os", config('_mssql_Port_env')),
    #     'USER': os.environ.get("_mssql_Login_os", config('_mssql_Login_env')),
    #     'PASSWORD': os.environ.get("_mssql_Password_os", config('_mssql_Password_env')),
    #     'OPTIONS': {
    #         'driver' : 'SQL Server Native Client 11.0',
    #         'MARS_Connection' : True,
    #         'driver_supports_utf8' : True,
    #     },
    # },
    # [H - setup] ################################
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("default_postgres_NAME", config('default_postgres_NAME')),
        'HOST': os.environ.get("default_postgres_HOST", config('default_postgres_HOST')),
        'USER': os.environ.get("default_postgres_USER", config('default_postgres_USER')),
        'PASSWORD': os.environ.get("default_postgres_PASSWORD", config('default_postgres_PASSWORD')),
        'PORT': os.environ.get("default_postgres_PORT", config('default_postgres_PORT')),
        'OPTIONS': {
            'options': '-c search_path=djangoanalytics'
        },
    },
    # [ALL - setup] ##############################
    'test_remote_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_remote_db.sqlite3',
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# LOGIN-LOGOUT ###################################
INACTIVE_TIME = 60*60  # in minutes - or whatever period you think appropriate
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = INACTIVE_TIME   # change expired session
SESSION_IDLE_TIMEOUT = INACTIVE_TIME  # logout

#Grappeli admin front-face
GRAPPELLI_ADMIN_TITLE = 'Администрирование DjangoAnalytics'
GRAPPELLI_SWITCH_USER = True

# LDAP authentification backend
LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/accounts/login'
LOGOUT_REDIRECT_URL = '/accounts/login'


# LDAP Authentification ##########################
# The URL of the LDAP server.
LDAP_AUTH_URL = config('LDAP_URL', default='') #LDAP_URL = ldap://domainName-something-something

# Initiate TLS on connection.
LDAP_AUTH_USE_TLS = False

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = f"dc={config('LDAP_SEARCH_BASE_dc1', default='')},\
                        dc={config('LDAP_SEARCH_BASE_dc2', default='')},\
                        dc={config('LDAP_SEARCH_BASE_dc3', default='')}"
#LDAP_SEARCH_BASE_dc1 = www
#LDAP_SEARCH_BASE_dc2 = domainName
#LDAP_SEARCH_BASE_dc3 = ru
# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"

# User model fields mapped to the LDAP
# attributes that represent them.
LDAP_AUTH_USER_FIELDS = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}    
LDAP_AUTH_OBJECT_CLASS = "user"

# A tuple of django model fields used to uniquely identify a user.
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)

# Path to a callable that takes a dict of {model_field_name: value},
# returning a dict of clean model data.
# Use this to customize how data loaded from LDAP is saved to the User model.
LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"

# Path to a callable that takes a user model and a dict of {ldap_field_name: [value]},
# and saves any additional user relationships based on the LDAP data.
# Use this to customize how data loaded from LDAP is saved to User model relations.
# For customizing non-related User model fields, use LDAP_AUTH_CLEAN_USER_DATA.
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"

# Path to a callable that takes a dict of {ldap_field_name: value},
# returning a list of [ldap_search_filter]. The search filters will then be AND'd
# together when creating the final search filter.
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"

# Path to a callable that takes a dict of {model_field_name: value}, and returns
# a string of the username to bind to the LDAP server.
# Use this to support different types of LDAP server.
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory_principal"

# Sets the login domain for Active Directory users.
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = config('LDAP_DOMAIN', default='') #LDAP_DOMAIN = www.examle.ru

# The LDAP username and password of a user for querying the LDAP database for user
# details. If None, then the authenticated user will be used for querying, and
# the `ldap_sync_users` command will perform an anonymous query.
LDAP_AUTH_CONNECTION_USERNAME = config('LDAP_USERNAME', default='')
LDAP_AUTH_CONNECTION_PASSWORD = config('LDAP_PASSWORD', default='')

# Set connection/receive timeouts (in seconds) on the underlying `ldap3` library.
LDAP_AUTH_CONNECT_TIMEOUT = None
LDAP_AUTH_RECEIVE_TIMEOUT = None


# Logging ########################################
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'filters': { 
        'require_debug_false': {         
             '()': 'django.utils.log.RequireDebugFalse'        
         },        
        'require_debug_true': {         
             '()': 'django.utils.log.RequireDebugTrue'        
           }     
     },        
    'formatters': {
        "default": {
            "format": "%(asctime)s [%(levelname)s]: [module: %(name)s]: %(message)s [filename: %(filename)s: line: %(lineno)d]",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "default_short": {
            "format": "%(asctime)s [%(levelname)s]: [module: %(name)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },        
    "handlers": {
        "mail_admins": { 
            "level": "ERROR", 
            "filters": ["require_debug_false"], 
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True, 
        }, 
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "default_short",
        },        
        "production_file": { 
            "level": "INFO", 
            "class": "logging.handlers.RotatingFileHandler", 
            "filename": BASE_DIR / 'logs/django/production.log',
            "maxBytes": 1024 * 1024 * 5,  # 5 MB 
            "backupCount": 1, 
            "formatter": "default", 
            "filters": ["require_debug_false"], 
        }, 
        "debug_file": { 
            "level": "DEBUG", 
            "class": "logging.handlers.RotatingFileHandler", 
            "filename": BASE_DIR / 'logs/django/debug.log',
            "maxBytes": 1024 * 1024 * 5,  # 5 MB 
            "backupCount": 1, 
            "formatter": "default", 
            "filters": ["require_debug_true"], 
        }, 
        "null": {
            "class": "logging.handlers.RotatingFileHandler", 
            "filename": BASE_DIR / 'logs/django/all.log',
            "maxBytes": 1024 * 1024 * 5,  # 5 MB 
            "backupCount": 1, 
            "formatter": "default", 
        }        
    },
    "loggers": {
        "django.request": { 
            "handlers": ["mail_admins", "console"], 
            "level": "ERROR", 
            "propagate": True, 
        }, 
        "django": { 
            "handlers": ["null", ], 
            "propagate": False,
        }, 
        "py.warnings": { 
            "handlers": ["null", ],
            "propagate": False, 
        },
        "django.security.DisallowedHost": {
            "handlers": ["null", ],
            "propagate": False,
        },        
        "django_python3_ldap": {
            "handlers": ["null", ],
            "propagate": True,
        },        
        "": {
            "handlers": ["console", "production_file", "debug_file"],
            "level": "DEBUG",
        }, 
    }
}

log = logging.getLogger("AUTH")

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):    
    # to cover more complex cases:
    # http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    ip = request.META.get('REMOTE_ADDR')

    log.debug('login user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))         

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs): 
    ip = request.META.get('REMOTE_ADDR')

    log.debug('logout user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    log.warning('login failed for: {credentials}'.format(
        credentials=credentials,
    ))


# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'        
        
        
        
        

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

FILE_CHARSET = 'utf-8-sig'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#initialize_base_content ##########################
#initialazie_base_content()
