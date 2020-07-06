from django.forms.models import model_to_dict

from .models import Combat, TYPES, TYPES_COMBAT, Field

from army_app.services import Army

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

    def __init__(self, combat_type, team_size, obstacles=[]):
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
                                             # obstacles=self.obstacles
                                             )
        return self

    @classmethod
    def load(cls, field):
        instance = cls.__new__(cls)
        setattr(instance, 'instance', field)
        setattr(instance, 'height', field.height)
        setattr(instance, 'width', field.width)
        # setattr(instance, 'obstacles', field.obstacles)
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

    def get_instance(self):
        assert hasattr(self, 'instance'), 'Fields object doesn\'t have instance.'
        return self.instance

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
    def create(cls, *, name, placement_time: int=3, placement_type: str = 'EQ', battle_type: str = 'DF',
               team_size: int = 1, started: bool = False, field: Fields):
        instance = cls.__new__(cls)
        combat = Combat.objects.create(name=name,
                                       placement_time=placement_time,
                                       placement_type=placement_type,
                                       battle_type=battle_type,
                                       team_size=team_size,
                                       started=started,
                                       field=field.get_instance())
        combat = Combat.objects.get(id=combat.id)
        for attr, value in model_to_dict(combat).items():
            if attr not in ['_state', 'left_team', 'right_team', 'mg_team']:
                setattr(instance, attr, value)
        setattr(instance, 'left_team', combat.left_team)
        setattr(instance, 'right_team', combat.right_team)
        setattr(instance, 'mg_team', combat.mg_team)
        setattr(instance, 'combat', combat)
        setattr(instance, 'field', field)
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
##############Change hero model to hero HEROES instance##############
    def start(self):
        assert hasattr(self, 'combat'), 'Combat instance doesn\'t provided.'
        assert self.start == False, 'Combat already started'
        # Initiate starting options
        self.gather_heroes()
        self.load_heroes_armyes()
        self.combat.started = True
        self.combat.save(update_fields=['started'])

    def load_heroes_armyes(self):
        assert hasattr(self, 'heroes'), 'No heroes in combat!'
        for id, hero in self.heroes:
            Army.load_army(hero)

    def gather_heroes(self):
        self.iter_id = 0
        for hero in self.left_team:
            self.create_hero_id(hero)
        for hero in self.right_team:
            self.create_hero_id(hero)
        for hero in self.mg_team:
            self.create_hero_id(hero)
#################################################################

    def create_hero_id(self, hero):
        if hasattr(self, 'heroes'):
            self.iter_id += 1
            self.heroes.update({
                self.iter_id: hero
            })
        else:
            self.heroes = {
                self.iter_id: hero
            }

    def get_hero(self, id):
        assert hasattr(self, 'heroes'), 'No heroes in combat!'
        return self.heroes[id]


class CombatHandler:

    def __init__(self, combat):
        self.combat = combat

    def handle(self, request):
        handler_output = {}
        self.validate_request(request)
        for item, value in request.items():
            if item == 'move':
                handler_output.update(self.move_handler(value))
            if item == 'attack':
                handler_output.update(self.attack_handler(value))
        return handler_output

    def move_handler(self, request):
        assert self.combat.start, 'Combat must be started'
        for hero_id, hero_value in request:
            hero = self.combat.get_hero(hero_id)
            for stack_id, stack_value in hero_value:
                stack = hero.army.get_stack(stack_id)
                stack.move()

    def attack_handler(self, request):
        assert self.combat.start, 'Combat must be started'
        for hero_id, hero_value in request:
            atacker_hero = self.combat.get_hero(hero_id)
            for stack_id, stack_value in hero_value:
                atacker_stack = atacker_hero.army.get_stack(stack_id)
                for enemy_hero_id, enemy_stack_id in stack_value:
                    enemy_hero = self.combat.get_hero(enemy_hero_id)
                    enemy_stack = enemy_hero.army.get_hero(enemy_stack_id)
                    atacker_stack.attack(enemy_stack)

    def units_data_get(self):
        pass

    def validate_request(self, request):
        """
        Переписать!
        :param request:
        :return:
        """
        for item, value in request.items():
            assert value, 'Handler can\'t be blank.'
            if item in ['move', 'attack']:
                assert 'hero_id' in value, 'No hero_id in handler.'
                value = value['hero_id']
                assert 'stack_id' in value, 'No stack_id in hero_id key.'
                value = value['stack_id']
                if item == 'move':
                    assert 'x' in value, 'No x coord provided in handler.'
                    assert 'y' in value, 'No y coord provided in handler.'
                    assert isinstance(value['x'], int), 'x must be integer.'
                    assert isinstance(value['y'], int), 'y must be integer.'
                if item == 'attack':
                    assert 'enemy_id' in value, 'No enemy_id in stack_id key.'
                    value = value['enemy_id']
                    assert 'enemy_stack_id' in value, 'No enemy_stack_id in enemy_id key.'
                    assert isinstance(value['enemy_stack_id'], int), 'enemy_stack_id must be integer.'


# Принцип работы обработчика:

# unit_identificator - [hero_id, stack_id]
#
a = {
    "move": {  # Move handler
        "hero_id": {
            'stack_id': {
                'x': 'int value',
                'y': 'int value',
            }
        },
    },
    'attack': {  # Attack handler
        "hero_id": {  # id юзера кто атаковал
            'stack_id': {  # id стака кто атаковал
                "enemy_id:int": "enemy_stack_id:int"
            }
        }
    },
}
