from django.forms.models import model_to_dict

from ..models import Combat, TYPES, TYPES_COMBAT

from .army import Army
from .field import Fields
from .hero import Heroes

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

    @classmethod
    def load(cls, combat: Combat):
        instance = cls.__new__(cls)
        for attr, value in model_to_dict(combat).items():
            if attr not in ['_state', 'left_team', 'right_team', 'mg_team']:
                setattr(instance, attr, value)
        setattr(instance, 'left_team', combat.left_team)
        setattr(instance, 'right_team', combat.right_team)
        setattr(instance, 'mg_team', combat.mg_team)
        setattr(instance, 'combat', combat)
        return instance

    @classmethod
    def create(cls, *, name, placement_time: int=3, placement_type: str = 'EQ', battle_type: str = 'DF',
               team_size: int = 1, started: bool = False, field: str):
        instance = cls.__new__(cls)
        combat = Combat.objects.create(name=name,
                                       placement_time=placement_time,
                                       placement_type=placement_type,
                                       battle_type=battle_type,
                                       team_size=team_size,
                                       started=started,
                                       field=field)
        for attr, value in model_to_dict(combat).items():
            if attr not in ['_state', 'left_team', 'right_team', 'mg_team']:
                setattr(instance, attr, value)
        setattr(instance, 'left_team', combat.left_team)
        setattr(instance, 'right_team', combat.right_team)
        setattr(instance, 'mg_team', combat.mg_team)
        setattr(instance, 'combat', combat)
        setattr(instance, 'field', Fields.get_field(battle_type=battle_type, team_size=team_size, name=field))
        return instance

    def set_name(self, name):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        self.combat.name = name
        self.combat.save(update_fields=['name'])
        self.name = name
        return self

    def add_hero_to_left_team(self, hero):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.battle_type == 'DF', 'Only default battle type provides left and right teams.'
        assert self.left_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self.left_team.add(hero)
        hero.in_battle = True
        hero.save(update_fields=['in_battle'])
        return self

    def add_hero_to_right_team(self, hero):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.battle_type == 'DF', 'Only default combat type provides left and right teams.'
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
        assert self.battle_type == 'MG', 'Only MeatGrinder combat type provides this method.'
        assert self.mg_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self.mg_team.add(hero)
        hero.in_battle = True
        hero.save(update_fields=['in_battle'])
        return self

    def start(self):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.started == False, 'Combat already started'
        # Initiate starting options
        self._gather_heroes()
        self._load_heroes_armyes()
        self.started = True
        self.combat.started = True
        self.combat.save(update_fields=['started'])

    def get_all_stacks(self):
        all_stacks = []
        for hero in self.heroes.values():
            all_stacks += hero.get_army().get_all_stacks()
        return all_stacks


    def get_hero(self, id):
        assert hasattr(self, 'heroes'), 'No heroes in combat!'
        return self.heroes[id]

    def get_stacks(self, hero_id, stack_id):
        assert self.started == True, 'Combat must be started.'
        return self.get_hero(hero_id).get_army().get_stack(stack_id)

    def _gather_heroes(self):
        self.iter_id = 0
        for hero in self.left_team.all():
            self._create_hero_id(hero)
        for hero in self.right_team.all():
            self._create_hero_id(hero)
        for hero in self.mg_team.all():
            self._create_hero_id(hero)

    def _load_heroes_armyes(self):
        assert hasattr(self, 'heroes'), 'No heroes in combat!'
        for id, hero in self.heroes.items():
            hero.gather_army()

    def _create_hero_id(self, hero):
        if hasattr(self, 'heroes'):
            self.iter_id += 1
            self.heroes.update({
                self.iter_id: Heroes.load_hero(hero)
            })
        else:
            self.heroes = {
                self.iter_id: Heroes.load_hero(hero)
            }

