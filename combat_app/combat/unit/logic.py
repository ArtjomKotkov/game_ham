import inspect


class UnitABS:
    """
    Base unit class.
    """
    name = 'Test'
    image = None
    health = 100
    min_attack = 1
    max_attack = 2
    defense = 0
    initiative = 15
    speed = 15
    icon = '/static/units/blank.png'
    army_cost = 0
    step_additionals = []
    big = False

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

    def _pos_in_step_radius(self, from_x, from_y, to_x, to_y):
        return True if ((to_x - from_x) ** 2 + (to_y - from_y) ** 2) ** (1 / 2) <= self.speed else False

    def base_movement(self, from_x, from_y, to_x, to_y):
        assert self._pos_in_step_radius(from_x, from_y, to_x, to_y), 'New position not in radius.'
        return to_x, to_y

    def get_unit_tiles(self, x, y):
        if self.big == False:
            return (x, y),
        else:
            return (x, y), (x+1, y), (x, y+1), (x+1), (y+1)

    def attack(self, identificator: str, self_unit, enemy_unit):
        output = {}
        assert self_unit.alive, 'Unit must be alive.'
        output_attack = enemy_unit.take_damage(self_unit)
        output.setdefault(identificator, {}).update(output_attack)
        return output

    def answer_attack(self, self_unit, enemy_unit, answer=True):
        output = {}
        #if self_unit.answer and self_unit.alive and self_unit.is_near(enemy_unit):
            #self_unit.answer = False
        self_unit.answer = answer
        output_attack = self.attack('attacker', self_unit, enemy_unit)
        output.update(output_attack)
        output.setdefault('modify', []).append('answer')
        return output

    def base_attack(self, self_unit, enemy_unit):
        output = self_unit.unit.attack(identificator='enemy', self_unit=self_unit, enemy_unit=enemy_unit)
        answer_output = enemy_unit.unit.answer_attack(self_unit=enemy_unit, enemy_unit=self_unit)
        output.update(answer_output)
        return output

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
        self.min_attack += value
        self.max_attack += value

    def add_defense(self, value):
        self.defense += value

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


class UnitAbstractClasses:

    class UnitDistanse(UnitABS):
        """
        Default distance unit.
        """
        name = 'UnitDistanse'

        def answer_attack(self, self_unit, enemy_unit, answer=False):
            output = {}
            if self_unit.is_near(enemy_unit):
                answer_output = super().answer_attack(self_unit, enemy_unit, answer) if self_unit.answer else {}
                output.update(answer_output)
            return output

    class UnitMelee(UnitABS):
        """
        Default melee unit.
        """

        name = 'UnitMelee'

        def base_attack(self, self_unit, enemy_unit):
            return super().base_attack(self_unit, enemy_unit) if self_unit.is_near(enemy_unit) else {}

        def answer_attack(self, self_unit, enemy_unit, answer=False):
            output = {}
            if self_unit.is_near(enemy_unit):
                answer_output = super().answer_attack(self_unit, enemy_unit, answer) if self_unit.answer else {}
                output.update(answer_output)
            return output


    class UnitMeleeDoubleAttack(UnitMelee):
        """
        Default melee unit.
        """
        name = 'UnitMeleeDoubleAttack'

        def base_attack(self, self_unit, enemy_unit):
            output = super().base_attack(self_unit, enemy_unit)
            if self_unit.is_near(enemy_unit):
                double_attack_output = self.attack('enemy-double', self_unit, enemy_unit)
                output.update(double_attack_output)
                output.setdefault('modify', []).append('double-attack')
            return output


    class UnitDistanceDoubleAttack(UnitDistanse):
        """
        Default melee unit.
        """
        name = 'UnitDistanceDoubleAttack'

        def base_attack(self, self_unit, enemy_unit):
            output = super().base_attack(self_unit, enemy_unit)
            double_attack_output = self.attack('enemy-double', self_unit, enemy_unit)
            output.update(double_attack_output)
            output.setdefault('modify', []).append('double-attack')
            return output


    class UnitDistanceAnswer(UnitDistanse):
        """
        Distance unit but make answer when somebody shoot or hit him.
        """
        name = 'UnitDistanceAnswer'

        def answer_attack(self, self_unit, enemy_unit, answer=True):
            output = {}
            output.setdefault('modify', []).append('range-answer')
            self_unit.answer = answer
            answer_output = self.attack('attacker', self_unit, enemy_unit)
            output.update(answer_output)

            return output

    class UnitUnlimitedAnswerMelee(UnitMelee):
        """
        Distance unit but make answer when somebody shoot or hit him.
        """
        name = 'UnitUnlimitedAnswerMelee'

        def answer_attack(self, self_unit, enemy_unit, answer=True):
            output = super().answer_attack(self_unit, enemy_unit, answer)
            return output

    class UnitUnlimitedAnswerDistance(UnitDistanceAnswer):
        """
        Distance unit but make answer when somebody shoot or hit him.
        """
        name = 'UnitUnlimitedAnswerDistance'

        def answer_attack(self, self_unit, enemy_unit, answer=True):
            output = super().answer_attack(self_unit, enemy_unit, answer)
            return output