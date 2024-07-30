from django.contrib import admin
from .models import CustomUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'date_joined')
    ordering = ('-date_joined', 'email')


admin.site.register(CustomUser, UserAdmin)
