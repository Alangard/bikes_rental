from django.contrib import admin
from api.bikes.models import Bike, Rental

# Register your models here.
class BikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'cost_per_minute')
    ordering = ('-id', 'name')

class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time', 'total_cost')
    ordering = ('-end_time', 'total_cost')


admin.site.register(Bike, BikeAdmin)
admin.site.register(Rental, RentalAdmin)
