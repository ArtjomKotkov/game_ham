from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Hero, Spell, DefaultHero


class HeroABS:
    default_attack = 0
    default_defense = 0
    default_mana = 0
    default_spell_power = 0
    default_initiative = 0

    def add_attack(self, value:int):
        if hasattr(self, 'hero'):
            self.hero.attack += value
            self.hero.save(update_fields=['attack'])
        return self

    def set_attack(self, value:int):
        if hasattr(self, 'hero'):
            self.hero.attack = value
            self.hero.save(update_fields=['attack'])
        return self

    def add_defense(self, value:int):
        if hasattr(self, 'hero'):
            self.hero.defense += value
            self.hero.save(update_fields=['defense'])
        return self

    def set_defense(self, value:int):
        if hasattr(self, 'hero'):
            self.hero.defense = value
            self.hero.save(update_fields=['defense'])
        return self

    def add_mana(self, value:int):
        if hasattr(self, 'hero'):
            self.hero.mana += value
            self.hero.save(update_fields=['mana'])
        return self

    def set_mana(self, value:int):
        if hasattr(self, 'hero'):
            self.hero.mana = value
            self.hero.save(update_fields=['mana'])
        return self

    def add_spell_power(self, value:int):
        if hasattr(self, 'hero'):
            self.hero.spell_power += value
            self.hero.save(update_fields=['spell_power'])
        return self

    def set_spell_power(self, value:int):
        if hasattr(self, 'hero'):
            self.hero.spell_power = value
            self.hero.save(update_fields=['spell_power'])
        return self

    def add_initiative(self, value):
        if hasattr(self, 'hero'):
            self.hero.initiative += value
            self.hero.save(update_fields=['initiative'])
        return self

    def set_initiative(self, value):
        if hasattr(self, 'hero'):
            self.hero.initiative = value
            self.hero.save(update_fields=['initiative'])
        return self

    def add_spell(self, pk):
        if hasattr(self, 'hero'):
            spell = Spell.objects.get(pk=pk)
            self.hero.spells.add(spell)
            self.hero.save(update_fields=['spells'])
        return self

    def remove_spell(self, pk):
        if hasattr(self, 'hero'):
            spell = Spell.objects.get(pk=pk)
            self.hero.spells.remove(spell)
            self.hero.save(update_fields=['spells'])
        return self

    def clear_spells(self):
        if hasattr(self, 'hero'):
            self.hero.spells.clear()
            self.hero.save(update_fields=['spells'])
        return self


class HeroesCreate(HeroABS):

    @classmethod
    def create_empty_hero(cls, user, hero_name):
        hero = Hero.objects.create(
            user=user,
            name=hero_name,
            attack=cls.default_attack,
            defense=cls.default_attack,
            mana=cls.default_mana,
            spell_power=cls.default_spell_power,
            initiative=cls.default_initiative,
        )
        return hero

    @classmethod
    def create_hero(cls, user, default_hero, hero_name):
        hero = Hero.objects.create(
            user=user,
            name=hero_name,
            attack=default_hero.attack,
            defense=default_hero.defense,
            mana=default_hero.mana,
            spell_power=default_hero.spell_power,
            initiative=default_hero.initiative,
        )
        hero.spells.add(*default_hero.spells.all())
        hero.save()
        return hero

    @classmethod
    def create(cls, user, hero_name, hero_class=None):
        instance = cls.__new__(cls)
        if user.heroes.count() >= 3:
            raise serializers.ValidationError('User can\'t have more then 3 heroes')
        if not hero_class:
            hero = HeroesCreate.create_empty_hero(user, hero_name)
        else:
            try:
                try:
                    id = int(hero_class)
                except (TypeError, ValueError):
                    id = None
                default_hero = DefaultHero.objects.get(Q(name__iexact=hero_class) | Q(id=id))
                hero = HeroesCreate.create_hero(user, default_hero, hero_name)
            except DefaultHero.DoesNotExist:
                hero = HeroesCreate.create_empty_hero(user, hero_name)
        setattr(instance, 'hero', hero)
        return instance

    @classmethod
    def load_hero(cls, pk):
        instance = cls.__new__(cls)
        hero = Hero.objects.get(pk=pk)
        setattr(instance, 'hero', hero)
        return instance

    def get_hero(self):
        return self.hero if hasattr(self, 'hero') else None

class Heroes:

    class objects(HeroesCreate):
        pass
