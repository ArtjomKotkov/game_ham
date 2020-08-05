from django.forms.models import model_to_dict

from ..models import Combat, COMBAT_STATUSES

from .field import Fields
from .hero.basic import Heroes
from .combat_queue import CombatQueue

#Main decorators
def pre_action_validation_stack(function):
    """
    Pre action validation, when combat must be started and war was began.
    """

    def wrap(*args, **kwargs):
        self = args[0]
        assert isinstance(self, Combats), 'Decorator must be used in Combats class.'
        assert self.combat.is_started == True, 'Combat must be started.'
        assert self.combat.status == 'inbattle', 'Combat status must be in battle.'
        hero_id = args[1]
        unit_id = args[2]
        print(args)
        assert self.queue.is_stack_turn(hero_id, unit_id), 'Invalid unit was provided!!!'
        output = function(*args, **kwargs)
        return output

    return wrap

def pre_action_validation_hero(function):
    """
    Pre action validation, when combat must be started and war was began.
    """

    def wrap(*args, **kwargs):
        self = args[0]
        assert isinstance(self, Combats), 'Decorator must be used in Combats class.'
        assert self.combat.is_started == True, 'Combat must be started.'
        assert self.combat.status == 'inbattle', 'Combat status must be in battle.'
        hero_id = args[1]
        assert self.combat.queue.is_hero_turn(hero_id), 'Invalid unit was provided!!!'
        output = function(*args, **kwargs)
        return output

    return wrap

class Combats:

    def __init__(self, combat):
        self.initiative_list = []
        self.total_units = 0
        self.current_unit = None
        self.combat = combat
        self.field = Fields.get_field(battle_type=self.combat.battle_type, team_size=self.combat.team_size,
                                      name=self.combat.field)
        self.turn = 0
        if self.combat.is_started == True:
            self.start(force=True)

    @classmethod
    def create(cls, *, name, placement_time: int = 3, placement_type: str = 'EQ', battle_type: str = 'DF',
               team_size: int = 1, field: str = 'Simple'):
        assert Fields.check_field_is_aviable(battle_type=battle_type, team_size=team_size, name=field)[
            0], 'Invalid field name!'
        combat = Combat.objects.create(name=name,
                                       placement_time=placement_time,
                                       placement_type=placement_type,
                                       battle_type=battle_type,
                                       team_size=team_size,
                                       field=field)
        return Combats(combat)

    def set_status(self, status):
        self.combat.set_status(status)

    def start(self, force=False):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        if not force:
            assert self.combat.is_started == False, 'Combat already started'
        # Initiate starting options
        self._gather_heroes()
        self._load_heroes_armyes()
        self.set_status('load')

        setattr(self, 'queue', CombatQueue(combat=self))

    def combat_info(self):

        dict_ = {
            'battle_type': self.combat.battle_type,
            'placement_time': self.combat.placement_time,
            'team_size': self.combat.team_size,
            'field': Fields.full_serialize(self.field)
        }
        if self.combat.status == 'inbattle':
            dict_.update({
                'heroes': {id: hero.start_serialize() for id, hero in self.heroes.items()}
            })
        return dict_

    def _gather_heroes(self):
        self.iter_id = 0
        for hero in self.combat.left_team.all():
            self._create_hero_id(hero)
            setattr(hero, 'team', 'left')
        for hero in self.combat.right_team.all():
            self._create_hero_id(hero)
            setattr(hero, 'team', 'right')
        for hero in self.combat.mg_team.all():
            self._create_hero_id(hero)
            setattr(hero, 'team', 'mg')

    def _load_heroes_armyes(self):
        assert hasattr(self, 'heroes'), 'No heroes in combat!'
        for id, hero in self.heroes.items():
            hero.gather_army()

    def _create_hero_id(self, hero):
        if hasattr(self, 'heroes'):
            self.iter_id += 1
            self.heroes.update({
                self.iter_id: Heroes.load_hero(hero, combat=self)
            })
        else:
            self.heroes = {
                self.iter_id: Heroes.load_hero(hero, combat=self)
            }

    # Basic mechanics
    @pre_action_validation_stack
    def stack_attack(self, attacker_hero_id, attacker_unit_id, enemy_hero_id, enemy_unit_id):
        attacker_stack = self.get_stack(attacker_hero_id, attacker_unit_id)
        enemy_stack = self.get_stack(enemy_hero_id, enemy_unit_id)
        return attacker_stack.attack(enemy_stack)

    @pre_action_validation_hero
    def hero_attack(self, attacker_hero_id, enemy_hero_id, enemy_unit_id):
        attacker_hero = self.get_hero(attacker_hero_id)
        enemy_stack = self.get_stack(enemy_hero_id, enemy_unit_id)
        return attacker_hero.attack(enemy_stack)

    @pre_action_validation_stack
    def unit_move(self, hero_id, unit_id, to_x, to_y):
        stack = self.get_stack(hero_id, unit_id)

        # Check that new point in field.
        for to_x, to_y in stack.unit.get_unit_tiles(to_x, to_y):
            assert self.field.height >= to_y and self.field.width >= to_x and to_x > 0 and to_y > 0, 'This point is out of field.'
        # Check that new point is free.
        all_stacks = self.get_all_stacks()
        all_stacks.remove(stack)
        for combat_stack in all_stacks:
            for x, y in combat_stack.unit.get_unit_tiles(*combat_stack.get_pos()):
                assert x != to_x and y != to_y, 'This point isn\'t free,'

        return stack.move(to_x, to_y)

    # Units queries.
    def get_all_stacks(self):
        all_stacks = []
        for hero in self.heroes.values():
            all_stacks += hero.get_army().get_all_stacks()
        return all_stacks

    def get_hero(self, id):
        assert hasattr(self, 'heroes'), 'No heroes in combat!'
        return self.heroes[id]

    def get_stack(self, hero_id, stack_id):
        assert self.combat.is_started == True, 'Combat must be started.'
        return self.get_hero(hero_id).get_army().get_stack(stack_id)
