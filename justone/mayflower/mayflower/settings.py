TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-Ru'

SITE_ID = 1

USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%*o58m&749vr1u0%la(=p41t=8d6#x6y6$!v!^owmzo&fcrw)r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'mayflower.context_processor.back_call_processor',
    'mayflower.context_processor.main_menu_processor',
    'mayflower.context_processor.reviews_processor',
    'mayflower.context_processor.basket_processor',
    #'mayflower.context_processor.promo_slider_processor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mayflower.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mayflower.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    # 'robokassa',
    'walletone',
    'tinymce',
    'sorl.thumbnail',
    'mce_filebrowser',
    'redactor',

    'products',
    'order',
    'pages',
    'blog',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# fix for removed cookie with session_id
SESSION_SAVE_EVERY_REQUEST = True

# robokassa settings
# ROBOKASSA_LOGIN = 'MayFlo'
# ROBOKASSA_PASSWORD1 = 'aPnYNdYt?Dppp1@'
# ROBOKASSA_PASSWORD2 = 'Kb2$%ZS%@npgTDN'
# ROBOKASSA_STRICT_CHECK = True
# ROBOKASSA_TEST_MODE = False
# ROBOKASSA_USE_POST = True
# robokassa settings

# walletone settings
WALLETONE_MERCHANT_ID = 121218994666
WALLETTONE_USE_SIGNATURE = True
WALLETTONE_SIGNATURE = '6f4c59384732395147797c5e5731595a534766435070315b7b457a'
# walletone settings

try:
    from local_settings import *
except ImportError:
    pass

REDACTOR_OPTIONS = {
    'lang': 'ru',
    'removeStyles': 'false',
    'resize': 'true',
    'activebuttons': ['deleted', 'italic', 'bold', 'underline', 'unorderedlist', 'orderedlist',
                      'alignleft', 'aligncenter', 'alignright', 'justify'],
    'buttonSource': 'true',
    'plugins': ['table', 'video', 'fontcolor', 'fontfamily', 'fontsize'],
    'replaceDivs': False
}

REDACTOR_UPLOAD = 'uploads/'

#if DEBUG:
#    MIDDLEWARE_CLASSES += (
#        'mayflower.middleware.DebugMiddleware',
#    )

TINYMCE_DEFAULT_CONFIG = {
    'file_browser_callback': 'mce_filebrowser',
    'theme': "advanced",
    'width': 800,
    'height': 800,
    'relative_urls': False,
    'remove_script_host': True,
    'convert_urls': False,
    'valid_elements': '*[*]'
}