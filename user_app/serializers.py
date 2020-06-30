from rest_framework import serializers

from django.contrib.auth.models import User

from hero_app.serializers import HeroShortSerializer, HeroFullSerializer


class UserShortSerializer(serializers.ModelSerializer):

    heroes = HeroShortSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'heroes']

class UserFullSerializer(serializers.ModelSerializer):

    heroes = HeroFullSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'heroes']