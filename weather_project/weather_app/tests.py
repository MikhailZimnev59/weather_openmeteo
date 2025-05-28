
from django.test import TestCase, Client
from unittest.mock import patch
from .models import CitySearch, UserSearchHistory

class WeatherTests(TestCase):

    @patch('weather_app.views.get_lat_lon')
    @patch('weather_app.views.get_weather')
    def test_index_success(self, mock_get_weather, mock_get_lat_lon):
        mock_get_lat_lon.return_value = (55.7558, 37.6173)  # Москва
        mock_get_weather.return_value = {
            'current_weather': {
                'temperature': 20,
                'weathercode': 1,
                'windspeed': 5,
                'time': '2024-06-01T12:00'
            }
        }

        client = Client()
        response = client.post('/', {'city': 'Moscow'})
        self.assertContains(response, 'Погода в городе Moscow')
        self.assertContains(response, '20')
        self.assertTrue(CitySearch.objects.filter(city_name='moscow').exists())
        self.assertTrue(UserSearchHistory.objects.filter(city_name='Moscow').exists())

    def test_stats_api(self):
        CitySearch.objects.create(city_name='moscow', search_count=3)
        CitySearch.objects.create(city_name='spb', search_count=1)
        client = Client()
        response = client.get('/statsapi/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'moscow': 3, 'spb': 1})

