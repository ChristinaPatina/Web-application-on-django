from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = 'c2897900e1a2e23fcc8ee15b48897d94'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    all_cities = []
    len_cities = len(cities)
    for city in cities:
        len_cities -= 1
        if len_cities > 4:
            continue
        else:
            res = requests.get(url.format(city.name)).json()
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"], #Celsius
                'pressure': float("{0:.1f}".format(res["main"]["pressure"]/1.333)), # /1.333   millimeter of mercury
                'humidity': res["main"]["humidity"], # %
                'wind': res["wind"]["speed"], # meter/sec
                'icon': res["weather"][0]["icon"]
            }
            all_cities.append(city_info)

    context = {'all_info': reversed(all_cities), 'form': form}

    return render(request, 'weather/index.html', context)


def home(request):
    return render(request, 'weather/home.html')