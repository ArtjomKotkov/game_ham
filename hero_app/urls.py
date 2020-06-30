from django.urls import path

from .views import HeroApi


urlpatterns = [
   path('hero/', HeroApi.as_view()),
   path('hero/<pk>', HeroApi.as_view())
]