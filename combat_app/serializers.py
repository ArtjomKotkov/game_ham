from rest_framework import serializers

from .models import Combat
from hero_app.serializers import HeroShortSerializer


class CombatShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Combat
        fields = (
            'id', 'name', 'placement_time', 'placement_type', 'battle_type', 'left_team', 'right_team', 'mg_team',
            'team_size', 'status', 'field')

class CombatFullSerializer(serializers.ModelSerializer):

    left_team = HeroShortSerializer(many=True)
    right_team = HeroShortSerializer(many=True)
    mg_team = HeroShortSerializer(many=True)

    class Meta:
        model = Combat
        fields = (
            'id', 'name', 'placement_time', 'placement_type', 'battle_type', 'left_team', 'right_team', 'mg_team',
            'team_size', 'status', 'field')

class FieldsSerializer(serializers.Serializer):
    fields = serializers.JSONField()