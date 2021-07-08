import os 
from decouple import config
from flask import Flask
from flask_appbuilder.security.manager import (
    AUTH_OID,
    AUTH_REMOTE_USER,
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
)
from s3cache import S3Cache
from celery.schedules import crontab
from werkzeug.contrib.cache import RedisCache
import ldap

# Superset base dir
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# initial config var's
#login = os.getenv('login', config('login'))

# Superset base config
DEBUG = True
SILENCE_FAB = False
SHOW_STACKTRACE = True

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
LOG_LEVEL = 'DEBUG'
ENABLE_TIME_ROTATE = True
TIME_ROTATE_LOG_LEVEL = 'DEBUG'
FILENAME = os.path.join(BASE_DIR, 'superset_logs/superset.log')
ROLLOVER = 'midnight'
INTERVAL = 1
BACKUP_COUNT = 30

SUPERSET_WEBSERVER_DOMAINS = ['domain.name.ru']

ROW_LIMIT = 5000
SUPERSET_WORKERS = 4
SUPERSET_WEBSERVER_PORT = 8088

# Flask App secret key
SECRET_KEY = 'Rrwr3235g@sdf+233-1'

# Uncomment to setup Your App name
# APP_NAME = "My App Name"

# Uncomment to setup Setup an App icon
# APP_ICON = "static/img/logo.jpg"

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:username@127.0.0.1:5432/postgres?options=-c search_path=django_services"
#SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "superset.db")
HTTP_HEADERS = {'X-Frame-Options': 'SAMEORIGIN'}

# <iframe src="linkToYourDashBoard?standalone=true"></iframe>
#<iframe src="http://domain-name:8088/superset/dashboard/5/?standalone=true"></iframe>

# <!DOCTYPE html> <html> <body> 
# <iframe src= "http://domain-name:8088/superset/dashboard/5/?preselect_filters=%7B%2248%22%3A%7B%22Retailer_country%22%3A%5B%5D%2C%22Quarter%22%3A%5B%5D%2C%22Product%22%3A%5B%5D%7D%7Dstandalone=true" width="600" height="400" seamless frameBorder="0" scrolling="no"> 
# </iframe> <p>Your browser does not support iframes.</p> </iframe> </body> </html> 
# http://domain-name:8088/login?username=admin&redirect=/superset/dashboard/world_health/


SQLALCHEMY_TRACK_MODIFICATIONS = True
# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = False
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

SESSION_COOKIE_SAMESITE = None # One of [None, 'Lax', 'Strict']

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = 'Xqwe43+1adas-a89'

# Caching 
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300, # 1 day default (in secs)
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'hostname',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://hostname:6379/1',
}

# celery tasks
CELERYBEAT_SCHEDULE = {
    'cache-warmup-hourly': {
        'task': 'cache-warmup',
        'schedule': crontab(minute=0, hour='*'),  # hourly
        'kwargs': {
            'strategy_name': 'top_n_dashboards',
            'top_n': 5,
            'since': '7 days ago',
        },
    },
}

FEATURE_FLAGS = {
    "THUMBNAILS": True,
    "THUMBNAILS_SQLA_LISTENERS": True,
}

class CeleryConfig(object):
    BROKER_URL = "redis://hostname:6379/0"
    CELERY_IMPORTS = ("superset.sql_lab")
    CELERY_RESULT_BACKEND = "redis://hostname:6379/0"
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}


#CELERY_CONFIG = CeleryConfig
RESULT_BACKEND = RedisCache(
	host='redis',
	port=6379,
	key_prefix='superset_results')



# ----------------------------------------------------
# THUMBNAIL_CACHE
# ----------------------------------------------------



# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
AUTH_TYPE = AUTH_LDAP
#AUTH_ROLE_PUBLIC = "Public"
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Alpha"
AUTH_LDAP_SERVER = "ldap://servername"
AUTH_LDAP_SEARCH = "DC=domain,DC=domainname,DC=ru"
#AUTH_LDAP_APPEND_DOMAIN = ""
AUTH_LDAP_BIND_USER = "username"
AUTH_LDAP_BIND_PASSWORD = "qazxsw_edcvfr_123"
AUTH_LDAP_UID_FIELD = "sAMAccountName"
AUTH_LDAP_FIRSTNAME_FIELD = "givenName"
AUTH_LDAP_LASTNAME_FIELD = "sn"
AUTH_LDAP_EMAIL_FIELD = "mail"
AUTH_LDAP_USE_TLS = False
AUTH_LDAP_ALLOW_SELF_SIGNED = False

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = 'public'
RECAPTCHA_PRIVATE_KEY = 'private'
RECAPTCHA_OPTIONS = {'theme': 'white'}


ENABLE_KERBEROS_AUTHENTICATION=True
KERBEROS_KEYTAB="/etc/security/keytabs/superset.headless.keytab"
KERBEROS_PRINCIPAL=""
KERBEROS_REINIT_TIME_SEC=3600

# ---------------------------------------------------
# Roles config
# ---------------------------------------------------
# Grant public role the same set of permissions as for the GAMMA role.
# This is useful if one wants to enable anonymous users to view
# dashboards. Explicit grant on specific datasets is still required.
#PUBLIC_ROLE_LIKE_GAMMA = False


# ---------------------------------------------------
# Babel config for translations
# ---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = 'ru'
#BABEL_DEFAULT_LOCALE = 'en'
# Your application default translation path
BABEL_DEFAULT_FOLDER = 'babel/translations'
# The allowed translation for you app
LANGUAGES = {
	'ru': {'flag': 'ru', 'name': 'Russian'},
    'en': {'flag': 'us', 'name': 'English'},
}

# ---------------------------------------------------
# Image and file configuration
# ---------------------------------------------------
# The file upload folder, when using models with files
UPLOAD_FOLDER = BASE_DIR + "/app/static/uploads/"

# The image upload folder, when using models with images
IMG_UPLOAD_FOLDER = BASE_DIR + "/app/static/uploads/"

# The image upload url, when using models with images
IMG_UPLOAD_URL = "/static/uploads/"
# Setup image size default is (300, 200, True)
# IMG_SIZE = (300, 200, True)


# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
# APP_THEME = "bootstrap-theme.css"  # default bootstrap
# APP_THEME = "cerulean.css"
# APP_THEME = "amelia.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
# APP_THEME = "readable.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"
# APP_THEME = "spacelab.css"
# APP_THEME = "united.css"
# APP_THEME = "yeti.css"

CSV_EXPORT = {
    'encoding': 'utf_8_sig',
 }


#Caching Thumbnails

#This is an optional feature that can be turned on by activating it’s feature flag on config:
FEATURE_FLAGS = {
    "THUMBNAILS": True,
    "THUMBNAILS_SQLA_LISTENERS": True,
}


 # ALERS DASHBOARD NOTIFICATIONS
ENABLE_SCHEDULED_EMAIL_REPORTS = True

EMAIL_NOTIFICATIONS = True

SMTP_HOST = "email-smtp.eu-west-1.amazonaws.com"
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = "smtp_username"
SMTP_PORT = 25
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_MAIL_FROM = "name@main.ru"

EMAIL_REPORTS_USER = 'name'

ENABLE_ALERTS = True
