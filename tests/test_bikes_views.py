# test_bikes_views.py
from django.urls import reverse
import pytest
from rest_framework import status
from django.utils import timezone
from celery.result import AsyncResult

from api.bikes.models import Rental
from api.bikes.tasks import calculate_total_cost

@pytest.mark.django_db
def test_bike_list_view(api_client, bike):
    response = api_client.get('/api/bikes/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_rental_create_view(api_client, user, bike):

    data = {
        "bike": bike.id,
        "end_time": timezone.now() + timezone.timedelta(hours=1)
    }
    response = api_client.post('/api/bikes/rent/', data, format='json')

    print(response)
    assert response.status_code == status.HTTP_201_CREATED
    assert Rental.objects.count() == 1
    assert Rental.objects.get().bike == bike
    assert Rental.objects.get().end_time == data['end_time']
    assert Rental.objects.get().start_time is not None 

    bike.refresh_from_db()
    assert bike.status == 'rented'

@pytest.mark.django_db
def test_rental_create_view_invalid(api_client, user, bike):

    data = {
        "bike": bike.id,
        "end_time": timezone.now() - timezone.timedelta(hours=1)  # Invalid end_time
    }
    response = api_client.post('/api/bikes/rent/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_rental_back_view(api_client, user, bike, rental):
    bike.status = 'rented'
    bike.save()

    url = f'/api/bikes/return/{bike.id}/'
    
    response = api_client.put(url)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert 'status_url' in response.data
    bike.refresh_from_db() 
    assert bike.status == 'available'

@pytest.mark.django_db
def test_rental_cost_status_view(api_client, bike, user, rental):
    task_id = calculate_total_cost.delay(rental.id).id
    url = f'/api/bikes/rental-cost-status/{task_id}/'
    response = api_client.get(url)

    # Test for completed task
    state = AsyncResult(task_id).state
    response = api_client.get(url)

    if state == 'SUCCESS':
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == rental.id
        assert response.data['bike'] == bike.id
        assert response.data['user'] == user 
    elif state == 'PENDING':
        assert response.status_code == status.HTTP_202_ACCEPTED
    else:
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
