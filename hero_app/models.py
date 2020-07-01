from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class DefaultHero(models.Model):
    name = models.CharField(max_length=24, unique=True)
    attack = models.IntegerField(default=1)
    defense = models.IntegerField(default=0)
    mana = models.IntegerField(default=0)
    spell_power = models.IntegerField(default=0)
    initiative = models.FloatField(default=10)

    def __str__(self):
        return self.name

class Hero(models.Model):
    name = models.CharField(max_length=24, default='Странник')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='heroes', blank=True)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    mana = models.IntegerField(default=0)
    spell_power = models.IntegerField(default=0)
    initiative = models.FloatField(default=0)
    # Spells as self model, with foreignkey.

class SpellTome(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Spell(models.Model):
    tome = models.ForeignKey(SpellTome, related_name='spells', on_delete=models.SET_NULL, null=True)
    hero = models.ManyToManyField(Hero, related_name='spells', blank=True)
    default_hero = models.ManyToManyField(DefaultHero, related_name='spells', blank=True)
    name = models.CharField(max_length=30, unique=True)
    short_name = models.CharField(max_length=16, unique=True)
    description = models.TextField()
    damage_per_tail = models.IntegerField()
    SCHEME_CHOICES = [
        ('CROSS', 'Across'),
        ('RECTAN', 'Rectangle'),
        ('CF', 'Circumference'),
    ]
    scheme = models.CharField(max_length=10, choices=SCHEME_CHOICES)
    height = models.IntegerField(validators=[MinValueValidator(1)])
    width = models.IntegerField(validators=[MinValueValidator(1)])

    def save(self, *args, **kwargs):
        if self.scheme in ('CROSS', 'CF'):
            if self.height % 2 == 0:
                self.height -= 1
            if self.width % 2 == 0:
                self.width -= 1
            if self.scheme == 'CF':
                if self.width != self.height:
                    if self.height > self.width:
                        self.width = self.height
                    else:
                        self.height = self.width
        return super().save(*args, **kwargs)




