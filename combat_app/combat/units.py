import inspect


def add_or_create_list_in_dict(dict_: dict, key: str, value):
    if not key in dict_:
        dict_[key] = [value]
    else:
        dict_[key].append(value)

class UnitABS:
    """
    Base unit class.
    """
    name = 'abs'
    image = None
    health = 1
    min_attack = 0
    max_attack = 0
    defense = 0
    initiative = 0
    speed = 0

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
    def pos_in_step_radius(cls, from_x, from_y, to_x, to_y):
        return True if ((to_x - from_x)**2+(to_y-from_y)**2)**(1/2) <= cls.speed else False

    @classmethod
    def base_movement(cls, from_x, from_y, to_x, to_y):
        assert cls.pos_in_step_radius(from_x, from_y, to_x, to_y), 'New position not in radius.'
        return to_x, to_y

    @classmethod
    def answer_attack(cls, self_unit, enemy_unit):
        output = {}
        if self_unit.answer and self_unit.alive and self_unit.is_near(enemy_unit):
            self_unit.answer = False
            damage, killed_units = enemy_unit.take_damage(self_unit)
            output['self'] = {
                'get_damage': [damage],
                'killed_units': [killed_units]
            }
            add_or_create_list_in_dict(output, 'modify', 'answer')
        return output

    # Attack modificators.

    @classmethod
    def double_attack(cls, self_unit, enemy_unit):
        output = cls.base_attack(self_unit, enemy_unit)
        if self_unit.alive:
            damage, killed_units = enemy_unit.take_damage(self_unit)
            output['enemy']['get_damage'].append(damage)
            output['enemy']['killed_units'].append(killed_units)
            add_or_create_list_in_dict(output, 'modify', 'double_attack')
        return output

    @classmethod
    def base_attack(cls, self_unit, enemy_unit):
        damage, killed_units = enemy_unit.take_damage(self_unit)
        output = {
            'enemy': {
                'get_damage': [damage],
                'killed_units': [killed_units]
            },
        }
        answer_output = cls.answer_attack(enemy_unit, self_unit)
        output.update(answer_output)
        return output

    @classmethod
    def attack(cls, self_unit, enemy_unit):
        return cls.base_attack(self_unit, enemy_unit)

    def __str__(self):
        return self.name

# Additional abstract unit classes.
class UnitDistanse(UnitABS):
    """
    Default distance unit.
    """
    type = 'distance'

class UnitMelee(UnitABS):
    """
    Default melee unit.
    """
    type = 'melee'

    @classmethod
    def base_attack(cls, self_unit, enemy_unit):
        assert self_unit.is_near(enemy_unit), 'Melee unit must be near enemy.'
        damage, killed_units = enemy_unit.take_damage(self_unit)
        output = {
            'enemy': {
                'get_damage': [damage],
                'killed_units': [killed_units]
            },
        }
        answer_output = cls.answer_attack(enemy_unit, self_unit)
        output.update(answer_output)
        return output

class UnitDistanceAnswer(UnitDistanse):
    """
    Distance unit but make answer when somebody shoot or hit him.
    """
    @classmethod
    def answer_attack(cls, self_unit, enemy_unit):
        output = {}
        if self_unit.answer and self_unit.alive:
            self_unit.answer = False
            damage, killed_units = enemy_unit.take_damage(self_unit)
            output['self'] = {
                'get_damage': [damage],
                'killed_units': [killed_units]
            }
            if self_unit.is_near(enemy_unit):
                add_or_create_list_in_dict(output, 'modify', 'answer')
            else:
                add_or_create_list_in_dict(output, 'modify', 'range-answer')
        return output


class Unit:

    class Archer(UnitDistanse):
        name = 'Archer'
        image = None
        health = 15
        min_attack = 5
        max_attack = 7
        defense = 2
        initiative = 11
        speed = 4


    class DemonArcher(UnitDistanceAnswer):
        name = 'ELFArcher'
        image = None
        health = 22
        min_attack = 12
        max_attack = 19
        defense = 2
        initiative = 11
        speed = 3

    class Civlian(UnitMelee):
        name = 'ELFArcher'
        image = None
        health = 3
        min_attack = 2
        max_attack = 3
        defense = 0
        initiative = 10
        speed = 8


UNIT_CLASSES = {key: value for key, value in Unit.__dict__.items() if inspect.isclass(value)}