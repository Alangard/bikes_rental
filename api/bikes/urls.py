from django.urls import path
from .views import BikeListView, RentalCreateView, RentalBackView, RentalCostStatusView

urlpatterns = [
    path('', BikeListView.as_view(), name='bike-list'),
    path('rent/', RentalCreateView.as_view(), name='rental-create'),
    path('return/<int:pk>/', RentalBackView.as_view(), name='rental-return'),
    path('rental-cost-status/<str:task_id>/', RentalCostStatusView.as_view(), name='task-status'),
]