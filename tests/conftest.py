import os
import pytest
from django.conf import settings
from django.core.management import call_command

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        settings.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'TEST': {
                'MIRROR': False,
            },
            'TIME_ZONE': 'UTC',
            'ATOMIC_REQUESTS': False,
            'AUTOCOMMIT': True,
            'CONN_MAX_AGE': 0,
            'CONN_HEALTH_CHECKS': False,
            'OPTIONS': {},
        }
        call_command('migrate')

@pytest.fixture(autouse=True)
def enable_debug_mode(settings):
    settings.DEBUG = True
def django_db_modify_db_settings():
    pass

@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """
    Override the database setup to use in-memory SQLite.
    The django_db_blocker argument is needed to make sure the setting change
    is applied before any database access happens.
    """
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TIME_ZONE': 'UTC',
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': False,
        'OPTIONS': {},
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'TEST': {
            'MIRROR': False,
        },
    }
    with django_db_blocker.unblock():
        from django.core.management import call_command
        call_command('migrate')
