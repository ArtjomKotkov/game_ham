# from .services import Stack
from services import Stack


def add_or_create_list_in_dict(dict_: dict, key: str, value):
    if not key in dict_:
        dict_[key] = [value]
    else:
        dict_[key].append(value)

class UnitABS:
    name = 'abs'
    image = None
    health = 1
    min_attack = 0
    max_attack = 0
    defense = 0
    initiative = 0
    speed = 0
    attack_distance = 0

    def __dict__(self):
        return dict(
            name=self.name,
            image=self.image,
            health=self.health,
            min_attack=self.min_attack,
            max_attack=self.max_attack,
            defense=self.defense,
            initiative=self.initiative,
            speed=self.speed,
        )

    @classmethod
    def base_attack(cls, self_unit: Stack, enemy_unit: Stack):
        damage, killed_units = enemy_unit.take_damage(self_unit)
        output = {
            'enemy': {
                'damage': [damage],
                'killed_units': [killed_units]
            },
        }
        if enemy_unit.answer and enemy_unit.alive:
            enemy_unit.answer = False
            damage_enemy, killed_units_enemy = self_unit.take_damage(enemy_unit)
            output.update({
                'self': {
                    'damage': [damage_enemy],
                    'killed_units': [killed_units_enemy]
                },
                'modify': ['answer']
            })
        return output

    @classmethod
    def answer_attack(cls, self_unit: Stack, enemy_unit: Stack):
        output = {}
        if self_unit.answer and self_unit.alive:
            damage, killed_units = enemy_unit.take_damage(self_unit)
            output['enemy'] = {
                'enemy': {
                    'damage': [damage],
                    'killed_units': [killed_units]
                },
            }
            add_or_create_list_in_dict(output, 'modify', 'answer')
        return output

    @classmethod
    def double_attack(cls, self_unit: Stack, enemy_unit: Stack):
        output = cls.base_attack(self_unit, enemy_unit)
        damage, killed_units = enemy_unit.take_damage(self_unit)
        output['enemy']['damage'].append(damage)
        output['enemy']['killed_units'].append(killed_units)
        if 'modify' in output:
            output['modify'].append('double_attack')
        else:
            output['modify'] = ['double_attack']
        return output

    def __str__(self):
        return self.name


class Archer(UnitABS):
    name = 'Archer'
    image = None
    health = 15
    min_attack = 5
    max_attack = 7
    defense = 2
    initiative = 11
    speed = 4
    attack_distance = 60

    @classmethod
    def attack(cls, self_unit: Stack, enemy_unit: Stack):
        return cls.base_attack(self_unit, enemy_unit)


class ElfArcher(UnitABS):
    name = 'ElfArcher'
    image = None
    health = 8
    min_attack = 12
    max_attack = 19
    defense = 2
    initiative = 11
    speed = 4
    attack_distance = 60

    @classmethod
    def attack(cls, self_unit: Stack, enemy_unit: Stack):
        return cls.double_attack(self_unit, enemy_unit)