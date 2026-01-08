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
