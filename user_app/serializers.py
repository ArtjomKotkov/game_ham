from rest_framework import serializers

from django.contrib.auth.models import User

from hero_app.serializers import HeroShortSerializer, HeroFullSerializer


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff']

class UserFullSerializer(serializers.ModelSerializer):

    heroes = HeroFullSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'heroes']