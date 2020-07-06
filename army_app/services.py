import random
from .units import UNIT_CLASSES

class Stack:

    def __init__(self, unit_class, count: int):
        self.unit = unit_class
        self.start_count = count
        self.count = self.start_count
        self.alive = True if self.count > 0 else False
        self.answer = True
        self.last_unit_health = self.unit.health
        self.x_pos = 0
        self.y_pos = 0
        for item, value in self.unit().__dict__().items():
            setattr(self, item, value)
        self.bufs = []

    def initiate_turn(self):
        self.answer = True

    def buf_defense(self):
        pass

    def add_unit(self, count):
        self.count += count
        if self.count <= 0:
            self.alive = False
            self.count = 0
        return self

    def set_unit(self, count):
        self.count = count
        if self.count <= 0:
            self.alive = False
            self.count = 0
        return self

    def kill(self):
        self.alive = False
        self.count = 0

    def set_last_unit_health(self, value):
        self.last_unit_health = self.unit.health if value > self.unit.health else value

    def set_pos(self, x, y):
        assert x >= 0, 'X must be more or equal 0.'
        assert y >= 0, 'Y must be more or equal 0.'
        self.x_pos = x
        self.y_pos = y

    def defend(self):
        pass

    def defense_back(self):
        return (100-self.defense)/100

    def take_damage(self, stack):
        assert isinstance(stack, Stack)
        damage = int(random.randrange(stack.min_attack, stack.max_attack)*stack.count*self.defense_back())
        killed_units = 0
        if damage >= self.last_unit_health + self.unit.health * (self.count - 1):
            self.kill()
            self.last_unit_health = 0
        else:
            killed_units = (damage // self.unit.health)
            remainder = (damage % self.unit.health)
            self.add_unit(-killed_units)
            self.last_unit_health -= remainder
        return damage, killed_units

    def attack(self, enemy):
        return self.unit.attack(self, enemy)

    def move(self, x, y):
        self.x_pos, self.y_pos = self.unit.move(self, self.x_pos, self.y_pos, x, y)

    def __str__(self):
        return self.name

class Army:
    def __init__(self):
        self.units = {}
        self.max_id = None


    @classmethod
    def load_army(cls, hero_instance):
        instance = cls.__new__(cls)
        setattr(instance, 'units', {})
        setattr(instance, 'max_id', None)
        for unit, count in hero_instance.get_hero().army.items():
            assert unit in UNIT_CLASSES, f'Invalid unit class [{unit}]'
            stack = Stack(UNIT_CLASSES[unit], count)
            instance.add_stack(stack)
        setattr(hero_instance, 'combat_army', instance)
        return instance

    def increase_max_id(self):
        if self.max_id != None:
            self.max_id += 1
        else:
            self.max_id = 0

    def add_stack(self, stack:Stack):
        self.increase_max_id()
        self.units.update({
            self.max_id: stack
        })

    def split_stack(self, id, count):
        self.units[id].add_unit(-count)
        new_stack = Stack(self.units[id].unit, count)
        self.add_stack(new_stack)

    def del_stack(self, id):
        assert id in self.units, f'No stack with id {id}.'
        del self.units[id]

    def get_stack(self, id):
        assert id in self.units, f'No stack with id {id}.'
        return self.units[id]

    def __dict__(self):
        output_dict =  {
            'max_id':self.max_id,
        }
        for id, unit in self.units.items():
            output_dict.update({id:unit.__dict__})
        return output_dict

