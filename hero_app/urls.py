from django.urls import path

from .views import HeroApi, SpellsApi, SpelTomesApi


urlpatterns = [
   path('hero/', HeroApi.as_view()),
   path('hero/<pk>', HeroApi.as_view()),
   path('spell/', SpellsApi.as_view()),
   path('spell/<pk>', SpellsApi.as_view()),
   path('spell_tome/', SpelTomesApi.as_view()),
   path('spell_tome/<pk>', SpelTomesApi.as_view()),
]