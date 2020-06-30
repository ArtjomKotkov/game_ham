import re

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Hero, Spell, SpellTome
from .services import Heroes

# Spells serializers.
class SpellShortSerializer(serializers.ModelSerializer):
    tome = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = Spell
        fields = ['id', 'name', 'tome']

class SpellFullSerializer(serializers.ModelSerializer):
    tome = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = Spell
        fields = ['id', 'name', 'short_name', 'description',
                  'damage_per_tail', 'scheme', 'height', 'width', 'tome']

# SpellTomes serializers.
class SpellTomeShortSerializer(serializers.ModelSerializer):

    spells = SpellShortSerializer(many=True, read_only=True)

    class Meta:
        model = SpellTome
        fields = ['id', 'name', 'spells']

class SpellTomeFullSerializer(serializers.ModelSerializer):
    spells = SpellFullSerializer(many=True, read_only=True)

    class Meta:
        model = SpellTome
        fields = ['id', 'name', 'spells']


class CharOrIntField(serializers.Field):

    re_decimal = re.compile(r'\.0*\s*$')  # allow e.g. '1.0' as an int, but not '1.2'

    def __init__(self, **kwargs):
        self.is_str = False
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            data = int(self.re_decimal.sub('', str(data)))
            self.is_str = False
        except (ValueError, TypeError):
            data = str(data)
            self.is_str = True
        return data

    def to_representation(self, value):
        return int(value) if not self.is_str else str(value)

# Hero serializers.
class HeroCreateSerializer(serializers.Serializer):

    user = serializers.IntegerField(write_only=True)
    name = serializers.CharField(max_length=24)
    hero_class = CharOrIntField(write_only=True, allow_null=True, required=False)

    def create(self, validated_data):
        hero = Heroes.objects.create(user_id=validated_data.get('user'),
                      hero_name=validated_data.get('name'),
                      hero_class=validated_data.get('hero_class', None))
        return hero.get_hero()


class HeroShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hero
        fields = ['id', 'name']

class HeroFullSerializer(serializers.ModelSerializer):

    spells = SpellShortSerializer(many=True, read_only=True)
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')

    class Meta:
        model = Hero
        fields = ['id', 'user', 'name', 'attack', 'defense',
                  'mana', 'spell_power', 'initiative', 'spells']