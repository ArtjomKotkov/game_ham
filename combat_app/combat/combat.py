from django.forms.models import model_to_dict

from ..models import Combat

from .field import Fields
from .hero.basic import Heroes

def pre_action_validation(function):
    """
    Pre action validation, when combat must be started and war was began.
    """
    def wrap(*args, **kwargs):
        self = args[0]
        assert isinstance(self, Combats), 'Decorator must be used in Combats class.'
        assert self.started == True, 'Combat must be started.'
        assert self.in_battle == True, 'Combat status must be - in_battle.'
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
        self.started = combat.started
        self.status = None
        if combat.started == True:
            self.start(force=True)

    @classmethod
    def create(cls, *, name, placement_time: int = 3, placement_type: str = 'EQ', battle_type: str = 'DF',
               team_size: int = 1, started: bool = False, field: str):
        assert Fields.check_field_is_aviable(battle_type=battle_type, team_size=team_size, name=field)[
            0], 'Invalid field name!'
        combat = Combat.objects.create(name=name,
                                       placement_time=placement_time,
                                       placement_type=placement_type,
                                       battle_type=battle_type,
                                       team_size=team_size,
                                       started=started,
                                       field=field)
        return Combats(combat)

    def set_status_prepare(self):
        self.status = 'prepare'

    def set_status_in_battle(self):
        self.status = 'in_battle'

    @property
    def in_battle(self):
        return True if self.status == 'in_battle' else False

    def set_status_ended(self):
        self.status = 'ended'

    def next_turn(self):
        pass

    def set_name(self, name):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        self.combat.name = name
        self.combat.save(update_fields=['name'])
        self.name = name
        return self

    def get_all_stacks(self):
        all_stacks = []
        for hero in self.heroes.values():
            all_stacks += hero.get_army().get_all_stacks()
        return all_stacks

    def get_hero(self, id):
        assert hasattr(self, 'heroes'), 'No heroes in combat!'
        return self.heroes[id]

    def get_stack(self, hero_id, stack_id):
        assert self.started == True, 'Combat must be started.'
        return self.get_hero(hero_id).get_army().get_stack(stack_id)

    def get_current_turn_unit(self):
        return self.initiative_list[self._init_next() - 1]

    def create_init_list(self):
        assert self.started == True, 'Combat must be started.'
        for id, hero in self.heroes.items():
            self._add_hero_to_initiate_list(hero)
            for stack in hero.get_army().get_all_stacks():
                self._add_stack_to_initiate_list(stack)
        self.sort_init_list()
        self.current_unit = 0

    def sort_init_list(self):
        self.initiative_list.sort(key=lambda x: x['initiative'], reverse=True)

    def start(self, force=False):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        if not force:
            assert self.started == False, 'Combat already started'
        # Initiate starting options
        self._gather_heroes()
        self._load_heroes_armyes()

        self.started = True
        self.combat.started = True
        self.combat.save(update_fields=['started'])

        self.create_init_list()

    def start_serilize(self):
        return {
            'battle_type': 'DF',
            'placement_time': 3,
            'team_size': 1
        }

    def _init_next(self):
        if self.current_unit + 1 == self.total_units:
            self.current_unit = 0
        else:
            self.current_unit += 1
        return self.current_unit

    def _add_hero_to_initiate_list(self, hero):
        self.initiative_list.append({
            'object': hero,
            'initiative': hero.initiative
        })
        self.total_units += 1

    def _add_stack_to_initiate_list(self, stack):
        self.initiative_list.append({
            'object': stack,
            'initiative': stack.unit.initiative
        })
        self.total_units += 1

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
    @pre_action_validation
    def unit_attack(self, attacker_hero_id, attacker_unit_id, enemy_hero_id, enemy_unit_id):
        attacker_stack = self.get_stack(attacker_hero_id, attacker_unit_id)
        enemy_stack = self.get_stack(enemy_hero_id, enemy_unit_id)
        return attacker_stack.attack(enemy_stack)

    @pre_action_validation
    def hero_attack(self, attacker_hero_id, enemy_hero_id, enemy_unit_id):
        attacker_hero = self.get_hero(attacker_hero_id)
        enemy_stack = self.get_stack(enemy_hero_id, enemy_unit_id)
        return attacker_hero.attack(enemy_stack)

    @pre_action_validation
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
