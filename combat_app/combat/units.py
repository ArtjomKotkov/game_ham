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
    icon = '/static/units/blank.png'
    army_cost = 0
    step_additionals = []

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
            cost=self.army_cost
        )

    @classmethod
    def pos_in_step_radius(cls, from_x, from_y, to_x, to_y):
        return True if ((to_x - from_x) ** 2 + (to_y - from_y) ** 2) ** (1 / 2) <= cls.speed else False

    @classmethod
    def base_movement(cls, from_x, from_y, to_x, to_y):
        assert cls.pos_in_step_radius(from_x, from_y, to_x, to_y), 'New position not in radius.'
        return to_x, to_y

    @classmethod
    def answer_attack(cls, self_unit, enemy_unit):
        output = {}
        print(f'{self_unit.answer=} {self_unit.alive=} {self_unit.is_near(enemy_unit)=}')
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
        answer_output = enemy_unit.unit.answer_attack(enemy_unit=enemy_unit, self_unit=self_unit)
        output.update(answer_output)
        return output

    @classmethod
    def move(cls, from_x, from_y, to_x, to_y):
        return cls.base_movement(from_x, from_y, to_x, to_y)

    @classmethod
    def attack(cls, self_unit, enemy_unit):
        return cls.base_attack(self_unit, enemy_unit)

    def __str__(self):
        return self.name

    @classmethod
    def serialize_short(cls, count=None):
        output = dict(
            name=cls.name,
            icon=cls.icon,
            cost=cls.army_cost
        )
        if count:
            output.update({'count': count})
        return output

    def base_defend(self):
        self.add_temp_defense(3, 1)

    def base_wait(self):
        self.add_temp_initiative(3, 1)

    def add_attack(self, value):
        self.attack += value

    def add_defense(self, value):
        self.defense += value

    def add_mana(self, value):
        self.mana += value

    def add_spell_power(self, value):
        self.spell_power += value

    def add_initiative(self, value):
        self.initiative += value

    def add_temp_attack(self, value, steps):
        self.add_attack(value)
        self.step_additionals.append({
            'method': self.add_attack,
            'attrs': [-value],
            'steps': steps
        })

    def add_temp_defense(self, value, steps):
        self.add_defense(value)
        self.step_additionals.append({
            'method': self.add_defense,
            'attrs': [-value],
            'steps': steps
        })

    def add_temp_mana(self, value, steps):
        self.add_mana(value)
        self.step_additionals.append({
            'method': self.add_mana,
            'attrs': [-value],
            'steps': steps
        })

    def add_temp_spell_power(self, value, steps):
        self.add_spell_power(value)
        self.step_additionals.append({
            'method': self.add_spell_power,
            'attrs': [-value],
            'steps': steps
        })

    def add_temp_initiative(self, value, steps):
        self.add_initiative(value)
        self.step_additionals.append({
            'method': self.add_initiative,
            'attrs': [-value],
            'steps': steps
        })

    def handle_turn(self):
        """
        Handle every turn of hero, delete temp parameters from hero.
        :return:
        """
        for additional in self.step_additionals:
            if additional['steps'] > 0:
                additional['steps'] -= 1
            else:
                additional['method'](*additional['attrs'])
                self.step_additionals.remove(additional)

# Additional abstract unit classes.
class UnitDistanse(UnitABS):
    """
    Default distance unit.
    """
    type = 'distance'

    @classmethod
    def attack(self, self_unit, enemy_unit):
        return super().attack(self_unit, enemy_unit)

    @classmethod
    def answer_attack(cls, self_unit, enemy_unit):
        return super().answer_attack(self_unit, enemy_unit)


class UnitMelee(UnitABS):
    """
    Default melee unit.
    """
    type = 'melee'

    @classmethod
    def attack(self, self_unit, enemy_unit):
        return super().attack(self_unit, enemy_unit)

    @classmethod
    def answer_attack(cls, self_unit, enemy_unit):
        return super().answer_attack(self_unit, enemy_unit)

    @classmethod
    def base_attack(cls, self_unit, enemy_unit):
        assert self_unit.is_near(enemy_unit), 'Melee unit must be near enemy.'
        return super().base_attack(self_unit, enemy_unit)


class UnitDistanceAnswer(UnitDistanse):
    """
    Distance unit but make answer when somebody shoot or hit him.
    """

    @classmethod
    def attack(self, self_unit, enemy_unit):
        return super().attack(self_unit, enemy_unit)

    @classmethod
    def answer_attack(cls, self_unit, enemy_unit):
        output = {}
        print(f'{self_unit.answer=} {self_unit.alive=}')
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
        human_readable = 'Лучник'
        name = 'Archer'
        health = 15
        min_attack = 5
        max_attack = 7
        defense = 2
        initiative = 11
        speed = 4
        icon = '/static/units/archer.png'
        army_cost = 250

    class DemonArcher(UnitDistanceAnswer):
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

    class Devil(UnitDistanceAnswer):
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

    class Civilian(UnitMelee):
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

    class Griffin(UnitMelee):
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
