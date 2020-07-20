import inspect

from .logic import UnitAbstractClasses as UAC
from .logic import UnitABS as TestUnit


class Unit:

    class Test(TestUnit):
        pass

    class Archer(UAC.UnitDistanse):
        human_readable = 'Лучник'
        name = 'Archer'
        health = 15
        min_attack = 5
        max_attack = 7
        defense = 2
        initiative = 11
        speed = 5
        icon = '/static/units/archer.png'
        army_cost = 250

    class DemonArcher(UAC.UnitDistanceAnswer):
        human_readable = 'Демон лучник'
        name = 'DemonArcher'
        image = None
        health = 22
        min_attack = 12
        max_attack = 19
        defense = 2
        initiative = 11
        speed = 3
        army_cost = 700

    class Devil(UAC.UnitMelee):
        human_readable = 'Черт'
        name = 'Devil'
        image = None
        health = 7
        min_attack = 1
        max_attack = 2
        defense = 1
        initiative = 12
        speed = 3
        army_cost = 60

    class Civilian(UAC.UnitMelee):
        name = 'Civilian'
        human_readable = 'Гражданин'
        image = None
        health = 3
        min_attack = 2
        max_attack = 3
        defense = 0
        initiative = 10
        speed = 8
        army_cost = 100

    class Griffin(UAC.UnitUnlimitedAnswerMelee):
        name = 'Griffin'
        human_readable = 'Грифон'
        image = None
        health = 3
        min_attack = 2
        max_attack = 3
        defense = 0
        initiative = 10
        speed = 8
        army_cost = 500


UNIT_CLASSES = {key: value for key, value in Unit.__dict__.items() if inspect.isclass(value)}