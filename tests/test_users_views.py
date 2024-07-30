# test_users_views.py
import pytest
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_create(api_client):
    url = reverse('register')  # Обновите на реальный путь
    data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password123',
    }
    
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().email == 'john.doe@example.com'
    assert User.objects.get().name == 'John Doe'

@pytest.mark.django_db
def test_obtain_jwt_token(api_client, user):
    
    url = reverse('token_obtain_pair')  # Обновите на реальный путь
    data = {
        'email': 'john.doe@example.com',
        'password': 'password123',
    }

    
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
