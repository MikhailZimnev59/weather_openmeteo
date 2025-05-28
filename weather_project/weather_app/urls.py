from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stats/', views.stats, name='stats'), # Вызов страницы со статистикой количеств вызовов по городам
    path('history/', views.history, name='history'), # История обращений к системе прогноз погоды
    path('statsapi/', views.stats_api, name='stats_api'), # Статистика вызовов (API)
]
