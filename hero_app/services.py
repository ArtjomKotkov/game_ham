from .models import Hero, Spell


class HeroABS:
    default_attack = 5
    default_defense = 0
    default_mana = 0
    default_spell_power = 0
    default_initiative = 10

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
    def create(cls, user):
        instance = cls.__new__(cls)
        hero = Hero.objects.create(
            user=user,
            attack=cls.default_attack,
            defense=cls.default_attack,
            mana=cls.default_mana,
            spell_power=cls.default_spell_power,
            initiative=cls.default_initiative,
        )
        setattr(instance, 'hero', hero)
        return instance


class HeroesLoad(HeroABS):

    @classmethod
    def load_hero(cls, pk):
        instance = cls.__new__(cls)
        hero = Hero.objects.get(pk=pk)
        setattr(instance, 'hero', hero)
        return instance


class Heroes:

    class Archer(HeroesCreate):
        default_attack = 14
        default_defense = 2
        default_mana = 0
        default_spell_power = 0
        default_initiative = 15

    class Knight(HeroesCreate):
        default_attack = 5
        default_defense = 20
        default_mana = 0
        default_spell_power = 0
        default_initiative = 12

    class Wizard(HeroesCreate):
        default_attack = 3
        default_defense = 4
        default_mana = 30
        default_spell_power = 5
        default_initiative = 13.5

    class Objects(HeroesLoad):
        pass