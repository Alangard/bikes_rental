from typing import Optional
from celery import shared_task
from django.utils import timezone
from datetime import datetime
from .models import Rental
from decimal import Decimal, ROUND_HALF_UP

@shared_task(retry_kwargs={'max_retries': 5})
def calculate_total_cost(rental_id: int) -> Optional[int]:
    try:
        rental = Rental.objects.get(id=rental_id)
    except Rental.DoesNotExist:
        return

    if rental.end_time and rental.start_time:
        duration = (rental.end_time - rental.start_time).total_seconds() / 60  # Duration in minutes
        duration = Decimal(duration)

        rental.total_cost = duration * rental.bike.cost_per_minute

        # Rounding to the nearest integer
        # total_cost = total_cost.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        rental.save()
        return rental.id # Return the rental ID or any identifier for the client to retrieve the rental later
    return None
