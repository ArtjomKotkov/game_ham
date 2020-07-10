from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import UserShortSerializer, UserFullSerializer
from hero_app.views import CustomAPIView

class UserPage(View):
    def get(self, request, username):
        context = {
            'owner': User.objects.get(username=username)
        }
        return render(request, 'user_app/user_page.html', context)

class UserApi(CustomAPIView):
    short_serializer = UserShortSerializer
    full_serializer = UserFullSerializer
    model = User
    available_methods = ['GET']