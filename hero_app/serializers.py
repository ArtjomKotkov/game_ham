from rest_framework import serializers

from .models import Hero, Spell, SpellTome


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

# Hero serializers.
class HeroShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hero
        fields = ['id', 'name']

class HeroFullSerializer(serializers.ModelSerializer):

    spells = SpellFullSerializer(many=True, read_only=True)

    class Meta:
        model = Hero
        fields = ['id', 'name', 'attack', 'defense',
                  'mana', 'spell_power', 'initiative', 'spells']