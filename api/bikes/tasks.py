from typing import Optional
from celery import shared_task
from django.utils import timezone
from django.db import transaction
from datetime import datetime
from .models import Rental
from decimal import Decimal, ROUND_HALF_UP

@shared_task(retry_kwargs={'max_retries': 5})
def calculate_total_cost(rental_id: int) -> Optional[int]:
    try:
        with transaction.atomic():
            rental = Rental.objects.select_for_update().get(id=rental_id)

            if rental.end_time and rental.start_time:
                duration = (rental.end_time - rental.start_time).total_seconds() / 60  # Duration in minutes
                duration = Decimal(duration)

                rental.total_cost = duration * rental.bike.cost_per_minute

                # Округление до ближайшего целого числа
                rental.total_cost = rental.total_cost.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                rental.save()

                return rental.id  # Возвращаем идентификатор аренды или любой другой идентификатор для клиента, чтобы позже получить аренду
    except Rental.DoesNotExist:
        return None

    return None
