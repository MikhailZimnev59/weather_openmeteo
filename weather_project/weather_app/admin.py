
from django.contrib import admin
from .models import CitySearch, UserSearchHistory

@admin.register(CitySearch)
class CitySearchAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'search_count', )

@admin.register(UserSearchHistory)
class UserSearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'city_name', 'searched_at', )

