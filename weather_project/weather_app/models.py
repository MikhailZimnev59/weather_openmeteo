'''Модели данных для накопления статистики и истории запросов'''

from django.db import models
class CitySearch(models.Model):
    '''Класс городов, которые были введены для получения прогноза и количество их вызовов'''

    city_name = models.CharField(max_length=100)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.city_name} ({self.search_count})"

class UserSearchHistory(models.Model):
    '''Класс накопления истории вызовов, города и время.
    По умолчанию сортируются в обратном порядке по времени вызова'''
    session_key = models.CharField(max_length=40)
    city_name = models.CharField(max_length=100)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']
