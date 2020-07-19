from django.forms.models import model_to_dict

from ..models import Combat, TYPES, TYPES_COMBAT

from .army import Army
from .field import Fields
from .hero import Heroes


class Combats:

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
        instance.initiative_list = []
        instance.total_units = 0
        instance.current_unit = None
        if combat.started == True:
            instance.start(force=True)
        return instance

    @classmethod
    def create(cls, *, name, placement_time: int = 3, placement_type: str = 'EQ', battle_type: str = 'DF',
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
        instance.initiative_list = []
        instance.total_units = 0
        instance.current_unit = None
        return instance

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
        return self.initiative_list[self._init_next()-1]

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

        self.create_init_list()

        self.combat.started = True
        self.combat.save(update_fields=['started'])
        delattr(self, 'left_team')
        delattr(self, 'right_team')
        delattr(self, 'mg_team')

    def begin_war(self):
        pass

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
        for hero in self.left_team.all():
            self._create_hero_id(hero)
            setattr(hero, 'team', 'left')
        for hero in self.right_team.all():
            self._create_hero_id(hero)
            setattr(hero, 'team', 'right')
        for hero in self.mg_team.all():
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
                self.iter_id: Heroes.load_hero(hero)
            })
        else:
            self.heroes = {
                self.iter_id: Heroes.load_hero(hero)
            }
