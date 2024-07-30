from django.db import models
from django.conf import settings

class Bike(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented')
    ]

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    cost_per_minute = models.DecimalField(max_digits=5, decimal_places=2, default=2.00)  # Cost per minute

    def __str__(self):
        return f"{self.id} - {self.status}"

class Rental(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Calculated cost

    def __str__(self):
        return f"{self.user.name} rented {self.bike.id}"
    