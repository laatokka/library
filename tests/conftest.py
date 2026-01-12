import os
import pytest
from django.conf import settings
from django.core.management import call_command
from testcontainers.postgres import PostgresContainer

@pytest.fixture(autouse=True)
def enable_debug_mode(settings):
    settings.DEBUG = True

@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """
    Override the database setup to use Postgres via Testcontainers.
    """
    with PostgresContainer("postgres:15") as postgres:
        from django.conf import settings

        # Configure Django to use the container
        settings.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': postgres.dbname,
            'USER': postgres.username,
            'PASSWORD': postgres.password,
            'HOST': postgres.get_container_host_ip(),
            'PORT': postgres.get_exposed_port(5432),
            'ATOMIC_REQUESTS': False,
            'AUTOCOMMIT': True,
            'OPTIONS': {},
            'TEST': {
                'MIRROR': None,
            },
            'TIME_ZONE': settings.TIME_ZONE,
            'CONN_HEALTH_CHECKS': False,
            'CONN_MAX_AGE': 0,
        }

        with django_db_blocker.unblock():
            from django.core.management import call_command
            call_command('migrate')
            yield
