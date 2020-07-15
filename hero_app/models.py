from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .levels import Levels
from combat_app.combat.hero import HEROES_CLASSES, HEROES_MODEL_CHOICES
from combat_app.combat.units import UNIT_CLASSES


class Hero(models.Model):
    name = models.CharField(max_length=24, default='Странник')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='heroes', blank=True)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    mana = models.IntegerField(default=0)
    spell_power = models.IntegerField(default=0)
    initiative = models.FloatField(default=0)
    in_battle = models.BooleanField(default=False)
    default = models.CharField(max_length=30, choices=HEROES_MODEL_CHOICES)
    army = models.JSONField(default=dict, blank=True)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    free_point = models.BooleanField(default=False)

    # Spells as self model, with foreignkey.

    def __str__(self):
        return f'{self.user.username}-{self.name}'

    @classmethod
    def _create_hero(cls, user, default_hero, hero_name, army: dict = None):
        default = HEROES_CLASSES[default_hero]
        if not army:
            army = {}
        hero = Hero.objects.create(
            user=user,
            name=hero_name,
            attack=default.attack,
            defense=default.defense,
            mana=default.mana,
            spell_power=default.spell_power,
            initiative=default.initiative,
            default=default_hero,
            army=army
        )
        hero.save()
        return hero

    @classmethod
    def create(cls, user, hero_name, hero_class, army=None):
        assert user.heroes.count() <= 3, 'User can\'t have more then 3 heroes'
        assert hero_class in HEROES_CLASSES, f'Invalid hero class - {hero_class}'
        hero = cls._create_hero(user, hero_class, hero_name, army)
        return hero

    def add_attack(self, value: int):
        self.attack += value
        self.save(update_fields=['attack'])

    def set_attack(self, value: int):
        self.attack = value
        self.save(update_fields=['attack'])

    def add_defense(self, value: int):
        self.defense += value
        self.save(update_fields=['defense'])

    def set_defense(self, value: int):
        self.defense = value
        self.save(update_fields=['defense'])

    def add_mana(self, value: int):
        self.mana += value
        self.save(update_fields=['mana'])

    def set_mana(self, value: int):
        self.mana = value
        self.save(update_fields=['mana'])

    def add_spell_power(self, value: int):
        self.spell_power += value
        self.save(update_fields=['spell_power'])

    def set_spell_power(self, value: int):
        self.spell_power = value
        self.save(update_fields=['spell_power'])

    def add_initiative(self, value):
        self.initiative += value
        self.save(update_fields=['initiative'])

    def set_initiative(self, value):
        self.initiative = value
        self.save(update_fields=['initiative'])

    def add_spell(self, pk):
        spell = Spell.objects.get(pk=pk)
        self.spells.add(spell)
        self.save(update_fields=['spells'])

    def remove_spell(self, pk):
        spell = Spell.objects.get(pk=pk)
        self.spells.remove(spell)
        self.save(update_fields=['spells'])

    def clear_spells(self):
        self.spells.clear()
        self.save(update_fields=['spells'])

    def set_unit_in_army(self, unit, count):
        assert unit in UNIT_CLASSES, 'Invalid unit class!'
        assert self._unit_can_be_added(unit, count), 'You can\'t add this count of units in army.'
        if count == 0:
            self._del_unit_from_army(unit)
        else:
            self.army[unit] = count
        self.save()

    def _set_unit_in_army(self, army, unit, count):
        assert unit in UNIT_CLASSES, 'Invalid unit class!'
        if count == 0:
            self._del_unit_from_army(unit)
        else:
            army[unit] = count

    def _calculate_army_power(self, army):
        power = 0
        for unit, count in army.items():
            power += UNIT_CLASSES[unit].army_cost * count
        return power

    def _unit_can_be_added(self, unit, count):
        temp_army = self.army.copy()
        self._set_unit_in_army(temp_army, unit, count)
        print(Levels.data['levels'][self.level]['army_power'],  self._calculate_army_power(temp_army))
        return True if Levels.data['levels'][self.level]['army_power'] >= self._calculate_army_power(temp_army) else False

    def _del_unit_from_army(self, unit):
        if unit in self.army:
            del self.army[unit]

    @property
    def available_stacks(self):
        return HEROES_CLASSES[self.default].get_available_stacks(self.level)

    @property
    def level_info(self):
        return Levels.data['levels'][self.level]

class SpellTome(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Spell(models.Model):
    tome = models.ForeignKey(SpellTome, related_name='spells', on_delete=models.SET_NULL, null=True)
    hero = models.ManyToManyField(Hero, related_name='spells', blank=True)
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
