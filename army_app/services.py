import random


class Army:
    def __init__(self):
        self.units = []

    def load_army(self, Hero):
        pass

    def add_stack(self, unit_class, count):
        for elem in self.units:
            if elem['class'] == unit_class:
                elem['count'] += count
                if elem['count'] <= 0:
                    del elem
                return
        self.units.append({
            'class': unit_class,
            'count': count
        })
        return self

    def split_stack(self, unit_class, count):
        assert unit_class in [elem['class'] for elem in self.units], 'This unit class doesn\'t exist.'
        for elem in self.units:
            if elem['class'] == unit_class:
                if count <= elem['count']:
                    self.add_stack(unit_class, -(elem['count']-count))
                    self.set_stack(unit_class, (elem['count']-count))

    def set_stack(self, unit_class, count):
        self.units.append({
            'class': unit_class,
            'count': count
        })
        return self

class Stack:

    def __init__(self, unit_class, count):
        self.unit = unit_class
        self.start_count = count
        self.count = self.start_count
        self.alive = True if self.count > 0 else False
        self.answer = True
        self.last_unit_health = self.unit.health

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
        self.alive = False
        self.count = 0

    def set_last_unit_health(self, value):
        self.last_unit_health = self.unit.health if value > self.unit.health else value

    def set_pos(self, x, y):
        assert x >= 0, 'X must be more or equal 0.'
        assert y >= 0, 'Y must be more or equal 0.'

    # def take_damage(self, count):
    #     if count >= self.last_unit_health + self.unit.health * (self.count-1):
    #         self.kill()
    #     else:
    #         killed_units = (count // self.unit.health)
    #         remainder = (count * self.unit.health)
    #         self.add_unit(-killed_units)
    #         self.last_unit_health -= remainder
    #
    # def attack(self, self_attack, enemy, enemy_attack):
    #     assert isinstance(enemy, Stack), 'Enemy param must be instance of Stack class.'
    #     enemy.take_damage(self_attack)
    #     if enemy.answer:
    #        self.take_damage(enemy_attack)

