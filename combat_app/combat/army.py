import random
from .unit.basic import UNIT_CLASSES


class Stack:

    def __init__(self, unit_class, count: int, hero=False):
        self.hero = hero
        self.unit = unit_class()
        if hero:
            self.unit_get_boosts_from_hero()
        self.start_count = count
        self.count = self.start_count
        self.alive = True if self.count > 0 else False
        self.answer = True
        self.last_unit_health = self.unit.health
        self.x_pos = 0
        self.y_pos = 0
        self.on_field = False

    def unit_get_boosts_from_hero(self):
        self.unit.add_initiative(self.hero.initiative*0.1)

    def initiate_turn(self):
        self.answer = True

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
        self.last_unit_health = 0
        self.alive = False
        self.count = 0

    def set_last_unit_health(self, value):
        self.last_unit_health = self.unit.health if value > self.unit.health else value

    def defend(self):
        return self.unit.base_defend()

    def defense_back(self):
        """
        Defense backend.
        :return:
        """
        return (100-self.unit.defense-self.hero.defense)/100 if self.hero else (100-self.unit.defense)/100

    def take_damage(self, enemy):
        assert isinstance(enemy, Stack), 'enemy must be STACK instance.'
        damage = int(random.randrange(enemy.unit.min_attack, enemy.unit.max_attack)*enemy.count*self.defense_back())
        killed_units = 0
        if damage >= self.last_unit_health + self.unit.health * (self.count - 1):
            killed_units = self.count
            self.kill()
        else:
            killed_units = (damage // self.unit.health)
            remainder = (damage % self.unit.health)
            self.add_unit(-killed_units)
            self.last_unit_health -= remainder
        return {
            'name': self.unit.name,
            'get_damage': damage,
            'killed_units': killed_units
        }

    def take_damage_from_hero(self, hero):
        """
        Damage calculate by using random, +-10% of hero damage.
        :param hero:
        :return:
        """
        damage = int((hero.attack+random.randrange(-0.1*hero.attack, 0.1*hero.attack))*self.defense_back())
        killed_units = 0
        if damage >= self.last_unit_health + self.unit.health * (self.count - 1):
            killed_units = self.count
            self.kill()
        else:
            killed_units = (damage // self.unit.health)
            remainder = (damage % self.unit.health)
            self.add_unit(-killed_units)
            self.last_unit_health -= remainder
        return damage, killed_units

    def attack(self, enemy):
        return self.unit.base_attack(self, enemy)

    def move(self, x, y):
        """
        :param x: x coord.
        :param y: y coord.
        :return:
        """
        assert x >= 0, 'X must be more or equal 0.'
        assert y >= 0, 'Y must be more or equal 0.'
        self.x_pos, self.y_pos = self.unit.base_movement(self.x_pos, self.y_pos, x, y)
        return self.x_pos, self.y_pos

    def set_pos(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def is_near(self, enemy):
        assert isinstance(enemy, Stack), 'Enemy must be STACK instance.'
        self_x, self_y = self.get_pos()
        enemy_x, enemy_y = enemy.get_pos()
        return True if ((self_x-enemy_x)**2+(self_y-enemy_y)**2)**(1/2) < 2 else False

    def get_pos(self):
        return self.x_pos, self.y_pos

    def __str__(self):
        return self.unit.name

    def serialize(self):
        return dict(
            x=self.x_pos,
            y=self.y_pos,
            unit=self.unit.__dict__(),
            start_count=self.start_count,
            count=self.count,
            alive=self.alive,
            answer=self.answer,
            last_unit_health=self.last_unit_health,
            on_field=self.on_field,
        )


class Army:

    def __init__(self, hero):
        self.units = {}
        self.max_id = None
        for unit, count in hero.get_hero().army.items():
            assert unit in UNIT_CLASSES, f'Invalid unit class [{unit}]'
            stack = Stack(UNIT_CLASSES[unit], count, hero)
            self.add_stack(stack)
        self.hero = hero

    def _increase_max_id(self):
        if self.max_id != None:
            self.max_id += 1
        else:
            self.max_id = 0

    def add_stack(self, stack:Stack):
        self._increase_max_id()
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

    def get_all_stacks(self):
        return [stack for stack in self.units.values()]

    def __dict__(self):
        output_dict =  {
            'max_id':self.max_id,
        }
        for id, unit in self.units.items():
            output_dict.update({id:unit.__dict__})
        return output_dict

    def serialize(self):
        return  {id:unit.serialize() for id, unit in self.units.items()}


