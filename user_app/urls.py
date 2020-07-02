from django.urls import path
from .views import UserPage

urlpatterns = [
    path('<str:username>/', UserPage.as_view(), name='user_page')
]