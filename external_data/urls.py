from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather_view, name='weather_view'),
    path('photo-test/', views.json_photo_view, name='photo_test'),
    path('api/weather-summary/', views.weather_summary_api, name='weather_summary_api'),
]
