import requests
from django.http import HttpResponseRedirect
from collections import OrderedDict
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from .models import City, Choice, Question
from .forms import CityForm
from django.urls import reverse
from django.views import generic


def index(request):
    appid = 'c2897900e1a2e23fcc8ee15b48897d94'
    weather = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    wiki_images = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&titles={}"

    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    all_cities = []
    for city in list(OrderedDict.fromkeys(reversed(cities))):
        if len(all_cities) >= 5:
            break

        weather_result = requests.get(weather.format(city.name)).json()
        if 'cod' in weather_result and weather_result["cod"] == '404':
            messages.error(request, 'Error: no city named ' + city.name)
            city.delete()
            continue

        city.name = weather_result["name"]
        city.save()

        wiki_result = requests.get(wiki_images.format(city.name.replace(' ', '_'))).json()
        src = 'http://www.polyplastic-piscine-34.com/images/no-images/no-image.jpg'
        try:
            src = list(wiki_result['query']['pages'].values())[0]['thumbnail']['source']
        except:
            print('heh well')

        city_info = {
            'city': weather_result["name"],
            'temp': weather_result["main"]["temp"],  # Celsius
            'pressure': float("{0:.1f}".format(weather_result["main"]["pressure"] / 1.333)),
            # /1.333   millimeter of mercury
            'humidity': weather_result["main"]["humidity"],  # %
            'wind': weather_result["wind"]["speed"],  # meter/sec
            'icon': weather_result["weather"][0]["icon"],
            'img': src
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)


def home(request):
    return render(request, 'weather/home.html')


def detail(request):
    question = get_object_or_404(Question, pk=1)
    return render(request, 'weather/detail.html', {'question': question})


def results(request):
    question = get_object_or_404(Question, pk=1)
    return render(request, 'weather/results.html', {'question': question})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'weather/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'weather/results.html'


def vote(request):
    question = get_object_or_404(Question, pk=1)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'weather/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('weather:results'))
