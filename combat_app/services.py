from .models import Combat, TYPES, TYPES_COMBAT, Field
from django.shortcuts import get_object_or_404


TYPES = [elem[0] for elem in TYPES]
# TYPES = (
#         ('free', 'Free'),
#         ('equal', 'Equal'),
#     )
DEFAULT_TYPE = 'free'
TYPES_COMBAT = [elem[0] for elem in TYPES_COMBAT]
# TYPES_COMBAT = (
#         ('1', '1vs1'),
#         ('2', '2vs2'),
#         ('3', '3vs3'),
#         ('MG', 'MeatGrinder'),
#     )
DEFAULT_TYPE_COMBAT = '1vs1'

class Fields:

    hero_placement_height = 8

    def __init__(self, combat_type, team_size, obstacles):
        """
        :param combat_type:
        :param hero_placement_height:
        :param team_size:
        :param obstacles: List of obstacles, every obstacle is a tuple with x, y cords of obstacle.
        [((x,y)),((x,y), (x,y), (x,y))]
        """
        self.combat_type = combat_type
        self.team_size = team_size
        self.height = self.calculate_field_height()
        self.width = self.calculate_field_width()
        self.obstacles = obstacles

    def create(self, name):
        self.instance = Field.objects.create(name=name,
                             height=self.height,
                             width=self.width,
                             #obstacles=self.obstacles
                             )
        return self.instance

    @classmethod
    def load(cls, field):
        instance = cls.__new__(cls)
        setattr(instance, 'instance', field)
        setattr(instance, 'height', field.height)
        setattr(instance, 'width', field.width)
        #setattr(instance, 'obstacles', field.obstacles)
        return instance

    def add_obstacle(self, obstacle: tuple):
        """
        :param obstacle:((x,y), (x,y))
        :return:
        """
        for coords in obstacle:
            assert len(coords) == 2, 'Coords must containt 2 values, x and y.'
            assert isinstance(coords[0], int), 'X value must be int.' + coords
            assert isinstance(coords[0], int), 'Y value must be int.' + coords
        self.obstacles.append(obstacle)

    def calculate_field_height(self):
        if self.combat_type == 'DF':
            height = self.hero_placement_height * self.team_size if self.team_size >= 2 else self.hero_placement_height * 2
        else:
            if self.team_size in [3, 4]:
                height = self.hero_placement_height + 10
            else:
                height = self.hero_placement_height * 2 + 12
        return height

    def calculate_field_width(self):
        if self.combat_type == 'DF':
            width = self.hero_placement_height * 2 + (self.team_size - 1) + 2

        else:
            if self.team_size in [3, 4]:
                width = self.hero_placement_height + 10
            else:
                width = self.hero_placement_height * 2 + 12
        return width

class Combats:

    def __init__(self, name=None):
        pass

    @classmethod
    def load(cls, combat: Combat):
        instance = cls.__new__(cls)
        for attr, value in combat.__dict__:
            if attr != '_state':
                setattr(instance, attr, value)
        return instance

    @classmethod
    def create(cls, *, name, placement_time, placement_type: str, battle_type: str, left_team: list, right_team: list,
               mg_team: list, team_size:int,  started:bool, field:Field, **kwargs):
        instance = cls.__new__(cls)
        combat = Combat.objects.create(**kwargs)
        for attr, value in combat.__dict__:
            if attr != '_state':
                setattr(instance, attr, value)
        setattr(instance, 'combat', combat)
        setattr(instance, 'field', Fields.load(field))
        return instance

    def set_name(self, name):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        self.combat.name = name
        self.combat.save(update_fields=['name'])
        self.name = name
        return self

    def add_hero_to_left_team(self, hero):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.combat_type == 'DF', 'Only default battle type provides left and right teams.'
        assert self.left_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self.left_team.add(hero)
        hero.in_battle = True
        hero.save(update_fields=['in_battle'])
        return self

    def add_hero_to_right_team(self, hero):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.combat_type == 'DF', 'Only default combat type provides left and right teams.'
        assert self.right_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self.combat.right_team.add(hero)
        hero.in_battle = True
        hero.save(update_fields=['in_battle'])
        return self

    def add_hero_to_combat(self, hero):
        """
        Add user on MeatGrinder combat.
        :param user:
        :return:
        """
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.combat_type == 'MG', 'Only MeatGrinder combat type provides this method.'
        assert self.mg_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self.mg_team.add(hero)
        hero.in_battle = True
        hero.save(update_fields=['in_battle'])
        return self

    def start(self):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.start == False, 'Combat already started'
        self.combat.started = True
        self.combat.save(update_fields=['started'])

    def units_data_get(self):
        pass
