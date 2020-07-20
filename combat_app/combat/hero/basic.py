import inspect

from .logic import HeroABS
from ..unit.basic import Unit


class Heroes:

    @classmethod
    def load_hero(cls, hero, combat):
        instance = HEROES_CLASSES[hero.default].__new__(HEROES_CLASSES[hero.default])
        setattr(instance, 'hero', hero)
        setattr(instance, 'combat', combat)
        return instance

    class Knight(HeroABS):
        name = 'Рыцарь'
        description = 'Типичный рыцарь'
        attack = 1
        defense = 3
        mana = 1
        spell_power = 0
        initiative = 12
        image = '/static/heroes/knight.jpg'
        aviable_stacks = {
            1: [Unit.Archer, Unit.Civilian],
            2: [Unit.Archer, Unit.Civilian, Unit.Griffin]
        }
        aviable_stacks_all = [Unit.Archer, Unit.Civilian, Unit.Griffin]

    class Demon(HeroABS):
        name = 'Демон'
        description = 'Типичный демон'
        attack = 5
        defense = 0
        mana = 0
        spell_power = 0
        initiative = 12
        image = '/static/heroes/demon.jpg'
        aviable_stacks = {
            1: [Unit.Devil],
            2: [Unit.Devil, Unit.DemonArcher]
        }
        aviable_stacks_all = [Unit.Devil, Unit.DemonArcher]

    class Elf(HeroABS):
        name = 'Эльф'
        description = 'Типичный эльф'
        attack = 2
        defense = 0
        mana = 0
        spell_power = 0
        initiative = 15
        image = '/static/heroes/elf.jpg'
        aviable_stacks = {
        }
        aviable_stacks_all = []

HEROES_CLASSES = {key: value for key, value in Heroes.__dict__.items() if inspect.isclass(value)}
HEROES_MODEL_CHOICES = tuple([(class_.__name__, class_.name) for class_ in HEROES_CLASSES.values()])