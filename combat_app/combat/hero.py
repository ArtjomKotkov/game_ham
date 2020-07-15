import inspect

from .army import Army
from .units import Unit


class HeroABS:
    name = 'Default'
    description = None
    attack = 0
    defense = 0
    mana = 0
    spell_power = 0
    initiative = 10
    aviable_stacks = []

    def get_hero(self):
        return self.hero if hasattr(self, 'hero') else None

    def get_army(self):
        return self.combat_army if hasattr(self, 'combat_army') else None

    def gather_army(self):
        assert hasattr(self, 'hero'), 'Hero doesn\'t loaded.'
        Army.load_army(self)

    @classmethod
    def get_available_stacks(cls, level):
        if level not in cls.aviable_stacks:
            return [{
                'name': unit.name,
                'cost': unit.army_cost
            } for unit in cls.aviable_stacks_all]
        else:
            return [{
                'name': unit.name,
                'cost': unit.army_cost
            } for unit in cls.aviable_stacks[level]]

    @classmethod
    def serialize(cls):
        units = [unit.serialize_short() for unit in cls.aviable_stacks]
        return dict(
            name=cls.name,
            description=cls.description,
            units=units,
            class_name=cls.__name__
        )

class Heroes:

    @classmethod
    def load_hero(cls, hero):
        instance = HEROES_CLASSES[hero.default].__new__(HEROES_CLASSES[hero.default])
        setattr(instance, 'hero', hero)
        return instance

    class Knight(HeroABS):
        name = 'Рыцарь'
        description = 'Типичный рыцарь'
        attack = 1
        defense = 3
        mana = 1
        spell_power = 0
        initiative = 12

        aviable_stacks = {
            1: [Unit.Archer, Unit.Civilian],
            2: [Unit.Archer, Unit.Civilian, Unit.Griffin]
        }
        aviable_stacks_all = [Unit.Archer, Unit.Civilian, Unit.Griffin]

    class Demon(HeroABS):
        name = 'Демон'
        description = 'Типичный демон'
        attack = 4
        defense = -1
        mana = 0
        spell_power = 0
        initiative = 13
        aviable_stacks = {
            1: [Unit.Devil],
            2: [Unit.Devil, Unit.DemonArcher]
        }
        aviable_stacks_all = [Unit.Devil, Unit.DemonArcher]


HEROES_CLASSES = {key: value for key, value in Heroes.__dict__.items() if inspect.isclass(value)}
HEROES_MODEL_CHOICES = tuple([(class_.__name__, class_.name) for class_ in HEROES_CLASSES.values()])