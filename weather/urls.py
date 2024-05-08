from django.urls import path 
from .views import  home,add_to_favourite, get_favourite_cities_weather,get_favourite_cities

urlpatterns = [
    path('', home, name = 'home'),
    path('add-to-favourite/', add_to_favourite, name='add_to_favourite'),
    path('get-weather-details/', get_favourite_cities_weather, name = 'get_favourite_cities_weather' ),
    path('get-favourite-cities/', get_favourite_cities, name='get_favourite_cities')
]