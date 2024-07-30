import pytest
from django.core.management import call_command
from celery import Celery
from rest_framework.test import APIClient
from django.utils import timezone

from api.bikes.models import Bike, Rental
from api.users.models import CustomUser

@pytest.fixture(scope='session', autouse=True)
def setup_and_teardown_db(django_db_setup, django_db_blocker):
    """Set up and tear down the database."""
    with django_db_blocker.unblock():
        # clear db before tests
        call_command('flush', verbosity=0, interactive=False)

    yield

    with django_db_blocker.unblock():
        # clear db after tests
        call_command('flush', verbosity=0, interactive=False)

@pytest.fixture(scope='session')
def celery_app():
    app = Celery('test_app')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True
    )
    return app

@pytest.fixture(scope='session')
def celery_worker(celery_app):
    from celery.contrib.testing.worker import start_worker
    return start_worker(celery_app)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(api_client):
    user = CustomUser.objects.create_user(email='john.doe@example.com', name='John Doe', password='password123')
    api_client.force_authenticate(user)
    return user

@pytest.fixture
def bike():
    return Bike.objects.create(status='available', name='bike1')

@pytest.fixture
def rental(user, bike):
    return Rental.objects.create(bike=bike, user=user, start_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(hours=1))
