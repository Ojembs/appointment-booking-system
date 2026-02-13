from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('confirm-booking/', views.booking_confirmation_view, name='confirm'),
    path('create/', views.create_booking_view, name='create'),
    path('<int:booking_id>/confirm/', views.confirm_booking_view, name='confirm_existing'),
    path('<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel'),
]