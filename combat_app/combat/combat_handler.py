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

    def _validate_request(self, request):
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

    def _movement_validator(self, x, y):
        stacks = self.combat.get_stacks()
        for stack in stacks:
            unit_x, unit_y = stack.get_pos()
            assert unit_x != x and unit_y != y, 'Tail is already taken.'

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
