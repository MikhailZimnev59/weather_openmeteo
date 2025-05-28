
import requests
from django.shortcuts import render, redirect
from .models import CitySearch, UserSearchHistory

NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
OPEN_METEO_URL = 'https://api.open-meteo.com/v1/forecast'

#Расшифровка кодов погоды, если в словаре нет, то выводится "Код не найден"

WC = {0: 'Ясное небо',                      1: 'В основном ясно', 2: 'Переменная облачность', 3: 'Пасмурно',    45: 'Туман',
      48: 'Иней или иней на земле',         51: 'Лёгкая морось',53: 'Умеренная морось', 55: 'Сильная морось',   56: 'Морось + замерзающая (лёгкая)',
      57: 'Морось + замерзающая (сильная)', 61: 'Лёгкий дождь', 63: 'Умеренный дождь',  65: 'Сильный дождь',    66: 'Дождь + замерзающий (лёгкий)',
      67: 'Дождь + замерзающий (сильный)',  71: 'Лёгкий снег',  73: 'Умеренный снег',   75: 'Сильный снег',     77: 'Град',
      80: 'Ливень — лёгкий',                81: 'Ливень — умеренный',                   82: 'Ливень — сильный', 85: 'Ливень со снегом — лёгкий',
      86: 'Ливень со снегом — сильный',     95: 'Гроза (обычная или слабая)',           96: 'Гроза + лёгкий град', 99: 'Гроза + сильный град'}

def get_lat_lon(city_name):
    # Геокодирование города через Nominatim
    params = {
        'q': city_name,
        'format': 'json',
        'limit': 1,
    }
    r = requests.get(NOMINATIM_URL, params=params, headers={'User-Agent': 'weather-application'})
    if r.status_code != 200 or not r.json():
        return None, None
    data = r.json()[0]
    return float(data['lat']), float(data['lon'])
import requests

def get_lat_lon_geocoding(city):
    # Геокодирование города через geocoding
    url = "https://geocoding-api.open-meteo.com/v1/search "
    params = {
        'name': city,
        'count': 1,
        'language': 'en',
        'format': 'json'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['results']:
        result = data['results'][0]
        return result['latitude'], result['longitude']
    else:
        raise Exception(f"City {city} not found")
def get_weather(lat, lon):
    # Получить погоду на ближайшее время (например, температуру, погода, время)
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m,weathercode',
        'current_weather': True,
        'timezone': 'auto',
    }
    r = requests.get(OPEN_METEO_URL, params=params)
    if r.status_code != 200:
        return None
    return r.json()

def index(request):
    context = {}
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    last_search = UserSearchHistory.objects.filter(session_key=session_key).order_by('-searched_at').first()
    if last_search:
        context['last_city'] = last_search.city_name

    if request.method == 'POST':
        city_name = request.POST.get('city', '').strip()
        if city_name:
            lat, lon = get_lat_lon(city_name)
            if lat is None:
                context['error'] = "Город не найден. Попробуйте ещё раз."
            else:
                weather_data = get_weather(lat, lon)
                if weather_data is None:
                    context['error'] = "Не удалось получить данные о погоде."
                else:
                    # Обновляем статистику поисков
                    city_obj, created = CitySearch.objects.get_or_create(city_name=city_name.lower())
                    city_obj.search_count += 1
                    city_obj.save()

                    # Сохраняем историю пользователя
                    UserSearchHistory.objects.create(session_key=session_key, city_name=city_name)

                    # Формируем вывод
                    current = weather_data.get('current_weather', {})
                    code = current.get('weathercode')
                    weather_code_name = WC.get(code, 'Код не найден').lower()
                    temp = current.get('temperature')
                    windspeed = current.get('windspeed')
                    time = current.get('time')

                    context.update({
                        'city_name': city_name,
                        'temperature': temp,
                        'weather_code': code,
                        'weather_code_name': weather_code_name,
                        'windspeed': windspeed,
                        'time': time,

                    })

    return render(request, 'weather_app/index.html', context)

from django.http import JsonResponse

def stats(request):
    ''' Статистика вызовов по городам, сортировка по убыванию количества вызовов'''

    stats = CitySearch.objects.all().order_by('-search_count')

    context = {
        'stats': stats,
    }
    return render(request, 'weather_app/stats.html', context)

def history(request):
    ''' История вызовов, сортировка по убыванию времени вызова '''

    hist = UserSearchHistory.objects.all().order_by('-searched_at')

    context = {
        'hist': hist,
    }
    return render(request, 'weather_app/history.html', context)

def stats_api(request):
    '''Статисика вызовов по городам (API)'''
    stats = CitySearch.objects.all()
    data = {c.city_name: c.search_count for c in stats}
    return JsonResponse(data)

