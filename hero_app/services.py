from .models import Hero


class HeroABS:
    default_attack = 5
    default_defense = 0
    default_mana = 0
    default_spell_power = 0
    default_initiative = 10

    # def create(self, user):
    #     if not hasattr(self, 'hero'):
    #         self.hero = Hero.object.create(
    #             user=user,
    #             attack=self.default_attack,
    #             defense=self.default_attack,
    #             mana=self.default_mana,
    #             spell_power=self.default_spell_power,
    #             initiative=self.default_initiative,
    #         )
    #     return self

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

    def load_hero(self, pk):
        self.hero = Hero.objects.get(pk=pk)
        return self

    def add_attack(self, value):
        if hasattr(self, 'hero'):
            self.hero.attack += value
            self.hero.save(update_fields=['attack'])
        return self

    def set_attack(self, value):
        if hasattr(self, 'hero'):
            self.hero.attack = value
            self.hero.save(update_fields=['attack'])
        return self

    def add_defense(self, value):
        if hasattr(self, 'hero'):
            self.hero.defense += value
            self.hero.save(update_fields=['defense'])
        return self

    def set_defense(self, value):
        if hasattr(self, 'hero'):
            self.hero.defense = value
            self.hero.save(update_fields=['defense'])
        return self

class Heroes:

    class Archer(HeroABS):
        default_attack = 14
        default_defense = 2
        default_mana = 0
        default_spell_power = 0
        default_initiative = 15

    class Knight(HeroABS):
        default_attack = 5
        default_defense = 20
        default_mana = 0
        default_spell_power = 0
        default_initiative = 12

    class Wizard(HeroABS):
        default_attack = 3
        default_defense = 4
        default_mana = 30
        default_spell_power = 5
        default_initiative = 13.5