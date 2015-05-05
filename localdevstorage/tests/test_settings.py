import os

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = TEST_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.staticfiles',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(TEST_DIR, 'static')

TEMPLATE_DIRS = (
    # Specifically choose a name that will not be considered
    # by app_directories loader, to make sure each test uses
    # a specific template without considering the others.
    os.path.join(TEST_DIR, 'test_templates'),
)


SECRET_KEY = "test"

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

MIDDLEWARE_CLASSES = []