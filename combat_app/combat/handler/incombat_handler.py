# from .field import Fields
# from .combat import Combats
# from ..serializers import CombatFullSerializer, CombatShortSerializer
# from ..models import Combat
from ..combat_manager import CombatManager


class InCombatHandler:

    manager = CombatManager()

    @staticmethod
    def read(request):
        assert isinstance(request, dict), 'request must be dict instance.'

        combat = InCombatHandler._init_combat(request)
        outcome = {}

        if 'action' in request:
            outcome.update(ActionHandler(combat).read(request['action']))

        if 'command' in request:
            outcome.update(CommandHandler(combat).read(request['command']))

        if 'system' in request:
            outcome.update(SystemHandler(combat).read(request['system']))

        return outcome

    @classmethod
    def _init_combat(cls, request):
        """Get combat instance for further using."""
        assert 'combat_id' in request, 'You must provide combat_id in request'
        return cls.manager.get_combat(request['combat_id'])



def func_name_adder(func):
    def first_wrapper(*args, **kwargs):
        self = args[0]
        output = func(*args, **kwargs)
        self.outcome.update({
            func.__name__: output
        })

    return first_wrapper



class BaseHandler:

    def __init__(self, combat):
        self.outcome = {}
        self.combat = combat

    @staticmethod
    def answer_template(paydict=None, status=None, message=None):
        """Template for answer."""
        assert status in (None, 'success', 'warning', 'error'), \
            'Invalid status! Available: None, success, warning, error'
        dict_ = dict()
        if paydict:
            dict_.update(dict(
                data=paydict
            ))
        if status:
            dict_.update(dict(
                status=status
            ))
        if message:
            dict_.update(dict(
                message=message
            ))
        return dict_


class ActionHandler(BaseHandler):
    """Handle actions of units and heroes."""

    def read(self, request):
        if 'attack' in request:
            self.attack(request['attack'])
        if 'move' in request:
            self.move(request['move'])
        return self.outcome

    @func_name_adder
    def attack(self, request):
        """Handle hero and stack attacks."""

        assert 'unit_type' in request, 'Unit_type must be provided in request.'
        assert request['unit_type'] in ['hero', 'stack'], 'Invalid unit type.'
        assert 'attacker_hero_id' in request, 'attacker_hero_id must be provided.'
        assert 'enemy_hero_id' in request, 'enemy_hero_id must be provided.'
        assert 'enemy_unit_id' in request, 'enemy_unit_id must be provided.'

        if request['unit_type'] == 'stack':
            assert 'attacker_unit_id' in request, 'attacker_unit_id must be provided.'
            return self.combat.stack_attack(request['attacker_hero_id'], request['attacker_unit_id'],
                                            request['enemy_hero_id'], request['enemy_unit_id'])

        elif request['unit_type'] == 'hero':
            return self.combat.hero_attack(request['attacker_hero_id'], request['enemy_hero_id'],
                                            request['enemy_unit_id'])

    @func_name_adder
    def move(self, request):
        """Handle stack movement."""
        assert 'hero_id' in request, 'hero_id must be provided.'
        assert 'unit_id' in request, 'unit_id must be provided.'
        assert 'to_x' in request, 'to_x must be provided.'
        assert 'to_y' in request, 'to_y must be provided.'

        x, y = self.combat.unit_move(request['hero_id'], request['unit_id'], request['to_x'], request['to_y'])
        return {
            'x': x,
            'y': y,
            'hero_id': request['hero_id'],
            'unit_id': request['unit_id']
        }

class CommandHandler(BaseHandler):
    """Handle commands from console."""

    def read(self, request):
        pass


class SystemHandler(BaseHandler):
    """Handle system requests."""

    def read(self, request):

        if 'list' in request:
            self.command_list(request['list'])
        if 'attr' in request:
            self.command_attr(request['attr'])
        return self.outcome

    # List functions.
    @func_name_adder
    def command_list(self, request):
        """Handle all commands which don't require any arguments."""
        outcome = []
        for command in request:
            if command == 'end':
                self.end(outcome)
            if command == 'next_turn':
                self.next_turn(outcome)
            if command == 'load':
                self.load(outcome)
        return outcome

    def load(self, list_):
        list_.append(self.answer_template(
            paydict=self.combat.combat_info(),
            status='success',
            message='load'
        ))

    def end(self, list_):
        list_.append(self.answer_template(
            paydict='nice',
            status='success',
            message='end'
        ))

    def next_turn(self, list_):
        return None

    # Attr functions.
    @func_name_adder
    def command_attr(self, request):
        """Handle all commands which require and arguments."""
        pass