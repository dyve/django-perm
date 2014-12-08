import django.conf.global_settings as DEFAULT_SETTINGS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

SECRET_KEY = 'ishalltellyouonlyonce'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'perm',
)

AUTHENTICATION_BACKENDS = DEFAULT_SETTINGS.AUTHENTICATION_BACKENDS + (
    # Object permissions using perm
    'perm.backends.ModelPermissionBackend',
)

# Django < 1.6 complains if this is not set
ROOT_URLCONF = 'perm.tests.urls'
SITE_ID = 1

# Django >= 1.7 complains if this is not set
MIDDLEWARE_CLASSES = DEFAULT_SETTINGS.MIDDLEWARE_CLASSES