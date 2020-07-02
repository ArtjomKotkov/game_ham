from django.urls import path

from .views import RegisterView, AuthView, logout_view

app_name = 'main_app'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('logout/', logout_view, name='logout'),
]