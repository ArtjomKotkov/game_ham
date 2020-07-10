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
        for credentials, value in request:
            stack = self.combat.get_stack(credentials[0], credentials[1])
            x, y = stack.move(x=value['x'], y=value['y'])
            return x, y

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
        pass

    def _movement_validator(self, x, y):
        stacks = self.combat.get_stacks()
        for stack in stacks:
            unit_x, unit_y = stack.get_pos()
            assert unit_x != x and unit_y != y, 'Tail is already taken.'
        assert self.combat.field.is_obstacle(x, y) == False, 'Tail is obstacle!'

# Принцип работы обработчика:

# unit_identificator - [hero_id, stack_id]
#
a = {
    "move": {  # Move handler
        ("hero_id", 'stack_id'): {
            'x': 'int',
            'y': 'int',
        },
    },
    'attack': {  # Attack handler
        ("enemy_id", 'enemy_id'): {
            "enemy_id:int": "enemy_stack_id:int"
        }
    },
    'admin': {
    }
}
