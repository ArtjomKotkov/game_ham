from rest_framework import serializers

from django.contrib.auth.models import User

from hero_app.serializers import HeroShortSerializer, HeroFullSerializer
from .models import HeroApp


class HeroAppShortSerilizer(serializers.ModelSerializer):
    class Meta:
        model = HeroApp
        fields = ['selected_hero']

class HeroAppFullSerilizer(serializers.ModelSerializer):

    selected_hero = HeroFullSerializer()

    class Meta:
        model = HeroApp
        fields = ['selected_hero']

class UserShortSerializer(serializers.ModelSerializer):

    heroapp = HeroAppFullSerilizer(many=False, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'heroapp']

class UserFullSerializer(serializers.ModelSerializer):

    heroes = HeroFullSerializer(many=True, read_only=True)
    heroapp = HeroAppShortSerilizer(many=False, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'heroes', 'heroapp']
        extra_kwargs = {'username': {'required': False}}

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key != 'heroapp':
                setattr(instance, key, value)
        if 'heroapp' in validated_data:
            if selected_hero:=validated_data['heroapp'].get('selected_hero', None):
                instance.heroapp.selected_hero = selected_hero
                instance.save()
        return instance