from rest_framework import serializers
from .models import Bike, Rental

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['id', 'name', 'status', 'cost_per_minute']


class RentalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rental
        fields = ['id', 'bike', 'user', 'start_time', 'end_time', 'total_cost']
        read_only_fields = ['start_time','total_cost', 'user']
