from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from hero_app.models import Hero

TYPES = (
        ('FR', 'Free'),
        ('EQ', 'Equal'),
        ('MG', 'MeatGrinder')
    )

TYPES_COMBAT = (
        ('DF', 'TeamVsTeam'),
        ('MG', 'MeatGrinder')
    )

class Field(models.Model):
    name = models.CharField(max_length=15)
    height = models.IntegerField(validators=[MinValueValidator(0)])
    width = models.IntegerField(validators=[MinValueValidator(0)])
    obstacles = models.JSONField(blank=True, default=list)

class Combat(models.Model):
    name = models.CharField(max_length=16)
    datetime = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True)
    placement_time = models.IntegerField(validators=[MinValueValidator(3)]) # Minutes for connect players.
    placement_type = models.CharField(choices=TYPES, default='EQ', max_length=2)
    battle_type = models.CharField(choices=TYPES_COMBAT, default='DF', max_length=2)
    left_team = models.ManyToManyField(Hero, blank=True, related_name='lt')
    right_team = models.ManyToManyField(Hero, blank=True, related_name='rt')
    mg_team = models.ManyToManyField(Hero, blank=True, related_name='mgt')
    team_size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], default=1, null=True)
    started = models.BooleanField(default=False)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self.battle_type == 'DF':
            assert self.team_size <= 3, 'In default battle type, team size can\'t be more then 3'
        if self.battle_type == 'MG':
            assert self.team_size >= 3, 'In meat grinder battle type, team size can\'t be less then 3'
        return super().save(*args, **kwargs)

