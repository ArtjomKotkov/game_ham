from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import RegisterView, AuthView, logout_view, HeroChooseView, HeroChooseApi

app_name = 'main_app'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('logout/', logout_view, name='logout'),
    path('hero/', HeroChooseView.as_view(), name='hero'),
    path('hero_api/', HeroChooseApi.as_view(), name='hero_api'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)