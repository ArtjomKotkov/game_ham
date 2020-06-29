from django.db import models
from django.contrib.auth.models import User


class Hero(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='heroes')
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    mana = models.IntegerField(default=0)
    spell_power = models.IntegerField(default=0)
    initiative = models.FloatField(default=0)
    # Spells as self model, with foreignkey.