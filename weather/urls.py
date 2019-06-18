from django.urls import path
from . import views

app_name = 'weather'
urlpatterns = [
    path('', views.home, name='home'),
    path('weather_info/', views.index, name='weather_info'),
    path('vote/detail/', views.detail, name='detail'),
    path('results/', views.results, name='results'),
    path('vote/', views.vote, name='vote'),
]
