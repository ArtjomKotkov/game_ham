from django.db import models

from hero_app.models import Hero

TYPES = (
        ('free', 'Free'),
        ('equal', 'Equal'),
    )

TYPES_COMBAT = (
        ('1', '1vs1'),
        ('2', '2vs2'),
        ('3', '3vs3'),
        ('MG', 'MeatGrinder'),
    )

class Combat(models.Model):
    name = models.CharField(max_length=16)
    datetime = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True)
    placement_type = models.CharField(choices=TYPES)
    battle_type = models.CharField(choices=TYPES_COMBAT)
    left_team = models.ManyToManyField(Hero, blank=True)
    right_team = models.ManyToManyField(Hero, blank=True)
    mt_team = models.ManyToManyField(Hero, blank=True)
