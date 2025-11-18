# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.get_weather, name='get_weather'),
    path('market-prices/', views.get_market_prices, name='get_market_prices'),
    path('featured-crops/', views.get_featured_crops, name='get_featured_crops'),
]