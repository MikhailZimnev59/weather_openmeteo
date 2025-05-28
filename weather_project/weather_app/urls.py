'''Маршруты приложения weather_app'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stats/', views.stats, name='stats'), # Вызов страницы со статистикой вызовов по городам
    path('history/', views.history, name='history'), # История обращений к системе прогноз погоды
    path('statsapi/', views.stats_api, name='stats_api'), # Статистика вызовов (API)
]
