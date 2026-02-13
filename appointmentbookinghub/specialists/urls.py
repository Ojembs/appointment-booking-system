from django.urls import path
from . import views

app_name = 'specialists'

urlpatterns = [
    path('', views.specialist_list_view, name='list'),
    path('<int:specialist_id>/', views.specialist_detail_view, name='detail'),
    path('<int:specialist_id>/calendar/', views.specialist_calendar_view, name='calendar'),
]
