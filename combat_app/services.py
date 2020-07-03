from .models import Combat, TYPES, TYPES_COMBAT
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


class Combats:

    def __init__(self, name=None):
        pass

    def load(self, combat:Combat):
        self.placement_type = combat.placement_type
        self.combat_type = combat.battle_type
        self.name = combat.name
        self._left_team = combat.left_team
        self._right_team = combat.right_team
        self._MG_stack = combat.mg_team
        self.field_height = combat.field_height
        self.field_width = combat.field_width
        self.hero_placement_height = combat.hero_placement_height
        self.team_size = combat.team_size
        self.started = combat.started
        self.combat = combat
        return self

    def create(self):
        assert not hasattr(self, 'combat'), 'Combat instance already exist.'
        assert hasattr(self, 'name') and hasattr(self, '_left_team') and hasattr(self, '_right_team') \
               and hasattr(self, '_MG_stack') and hasattr(self, '_MG_stack') and hasattr(self, 'combat_type') \
               and hasattr(self, 'placement_type'), 'Invalid combat credentials!'
        combat = Combat.objects.create(name=self.name,
                                       placement_type=self.placement_type,
                                       battle_type=self.combat_type,
                                       left_team=self._left_team,
                                       right_team=self._right_team,
                                       mg_team=self._MG_stack,
                                       hero_placement_height=self.hero_placement_height,
                                       field_width=self.field_width,
                                       field_height=self.field_height
                                       )
        setattr(self, 'combat', combat)
        return self

    def set_name(self, name):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        self.combat.name = name
        self.combat.save(update_fields=['name'])
        self.name = name
        return self

    def add_hero_to_left_team(self, hero):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.combat_type == 'DF', 'Only default battle type provides left and right teams.'
        assert self._left_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self._left_team.add(hero)
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
        assert self._MG_stack.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self._MG_stack.add(hero)
        hero.in_battle = True
        hero.save(update_fields=['in_battle'])
        return self

    def start(self):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.start == False, 'Combat already started'
        self.combat.started = True
        self.combat.save(update_fields=['started'])

    @classmethod
    def calculate_field_height(cls):
        if cls.combat_type == 'DF':
            height = cls.hero_placement_height * cls.team_size if cls.team_size >= 2 else cls.hero_placement_height*2
        else:
            if cls.team_size in [3, 4]:
                height = cls.hero_placement_height + 10
            else:
                height = cls.hero_placement_height * 2 + 12
        return height

    @classmethod
    def calculate_field_width(cls):
        if cls.combat_type == 'DF':
            width = cls.hero_placement_height * 2 + (cls.team_size-1)+2

        else:
            if cls.team_size in [3, 4]:
                width = cls.hero_placement_height + 10
            else:
                width = cls.hero_placement_height * 2 + 12
        return width