from ..army import Army


class HeroABS:
    name = 'Default'
    description = None
    attack = 0
    defense = 0
    mana = 0
    spell_power = 0
    initiative = 10
    aviable_stacks = []
    image = '/static/combat_app/units/blank.png'
    background = ''
    step_additionals = []
    team = None

    def get_hero(self):
        return self.hero if hasattr(self, 'hero') else None

    def get_army(self):
        return self.combat_army if hasattr(self, 'combat_army') else None

    def gather_army(self):
        assert hasattr(self, 'hero'), 'Hero doesn\'t loaded.'
        self.combat_army = Army(self)

    @classmethod
    def get_available_stacks(cls, level) -> list:
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
    def get_available_stacks_list(cls, level) -> list:
        if level not in cls.aviable_stacks:
            return [unit for unit in cls.aviable_stacks_all]
        else:
            return [unit for unit in cls.aviable_stacks[level]]

    @classmethod
    def serialize(cls):
        units = [unit.serialize_short() for unit in cls.aviable_stacks_all]
        return dict(
            name=cls.name,
            description=cls.description,
            units=units,
            class_name=cls.__name__,
            image=cls.image,
            stats={
                'Атака':cls.attack,
                'Защита':cls.defense,
                'Очки маны':cls.mana*10,
                'Сила заклинаний':cls.spell_power,
                'Инициатива':cls.initiative
            }
        )

    def start_serialize(self):
        return dict(
            name=self.name,
            team=self.team,
            description=self.description,
            army=self.combat_army.serialize(),
            class_name=self.__class__.__name__,
            image=self.image,
            stats={
                'Атака': self.attack,
                'Защита': self.defense,
                'Очки маны': self.mana * 10,
                'Сила заклинаний': self.spell_power,
                'Инициатива': self.initiative
            }
        )

    def base_attack(self, enemy_unit):
        damage, killed_units = enemy_unit.take_damage_from_hero(self)
        output = {
            'enemy': {
                'get_damage': [damage],
                'killed_units': [killed_units]
            },
        }
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
