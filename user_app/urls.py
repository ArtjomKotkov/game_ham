from django.urls import path
from .views import UserPage, UserApi

app_name='user'

urlpatterns = [
    path('info/<str:username>/', UserPage.as_view(), name='user_page'),
    path('', UserApi.as_view()),
    path('<pk>/', UserApi.as_view())
]