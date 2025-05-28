from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stats/', views.stats, name='stats'),
    path('history/', views.history, name='history'),
    path('statsapi/', views.stats_api, name='stats_api'),
]
