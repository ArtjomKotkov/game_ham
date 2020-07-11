import re

from rest_framework import serializers

from .models import Hero, Spell, SpellTome
from combat_app.combat.units import UNIT_CLASSES


# Spells serializers.
class SpellShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spell
        fields = ['id', 'name', 'tome']

class SpellFullSerializer(serializers.ModelSerializer):

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

class ArmyField(serializers.Field):

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        output = []
        for key, count in value.items():
            output.append(UNIT_CLASSES[key].serialize_short(count=count))
        print(output)
        return output


class HeroShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hero
        fields = ['id', 'name']

class HeroFullSerializer(serializers.ModelSerializer):
    """
    Spells fields in update methods must looks like:
    {
        "spells":{
            "remove":[...], | Delete spells from hero.
            "add":[...],    | Add spells to hero.
            "set":[...],    | Set hero spells.
        }
    }
    """
    spells = SpellShortSerializer(many=True, read_only=True)
    hero_class = CharOrIntField(write_only=True, allow_null=True, required=False)
    spells_manager = serializers.JSONField(write_only=True, required=False)
    army = ArmyField(read_only=True)

    class Meta:
        model = Hero
        fields = ['id', 'user', 'name', 'attack', 'defense',
                  'mana', 'spell_power', 'initiative', 'spells', 'hero_class', 'spells_manager', 'army']

    def create(self, validated_data):
        hero = Hero.create(user=validated_data.get('user', None),
                                     hero_name=validated_data.get('name', None),
                                     hero_class=validated_data.get('hero_class', None))
        return hero

    def update(self, instance, validated_data):
        if 'hero_class' in validated_data:
            del validated_data['hero_class']
        hero = super().update(instance, validated_data)
        if spells:= validated_data.get('spells_manager', None):
            remove = spells.get('remove', None)
            add = spells.get('add', None)
            set = spells.get('set', None)
            if remove:
                spells = Spell.objects.filter(id__in=remove)
                hero.spells.remove(*spells)
            if add:
                spells = Spell.objects.filter(id__in=add)
                hero.spells.add(*spells)
            if set:
                spells = Spell.objects.filter(id__in=set)
                hero.spells.set(spells, clear=True)
        return hero