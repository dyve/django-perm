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

