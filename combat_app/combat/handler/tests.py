import pprint

from django.contrib.auth.models import User
from django.test import TestCase

from ..combat import Combats
from ..combat_manager import CombatManager
from ..unit.basic import UNIT_CLASSES
from hero_app.models import Hero
from .incombat_handler import InCombatHandler


class TestsHandler(TestCase):

    def setUp(self) -> None:
        self.army1 = {
            'Test': 100,
        }
        self.army2 = {unit: 20 for unit in UNIT_CLASSES if unit != 'Test'}

        self.user1 = User.objects.create_user('test_user1', password='123456')
        self.user2 = User.objects.create_user('test_user2', password='123456')

        hero1 = Hero.create(user=self.user1, hero_name='test_hero_user_1', hero_class='Knight', army=self.army1)
        hero2 = Hero.create(user=self.user2, hero_name='test_hero_user_2', hero_class='Demon', army=self.army2)

        self.test_combat = Combats.create(name='test')

        self.test_combat.combat.add_hero_to_left_team(hero1)
        self.test_combat.combat.add_hero_to_right_team(hero2)
        self.test_combat.start()
        self.test_combat.set_status('inbattle')

        self.manager = CombatManager()
        self.manager.add_combat(self.test_combat)

    def test_func_name_decorator(self):
        example_request = {
            'combat_id': 1,
            'action': {
                'attack': {
                    'unit_type': 'stack',
                    'attacker_hero_id': 0,
                    'attacker_unit_id': 0,
                    'enemy_hero_id': 1,
                    'enemy_unit_id': 0
                }
            },
            'system': {
                'list': ['load', 'end']
            }
        }
        outcome = InCombatHandler.read(example_request)
        self.assertIn('command_list', outcome)
        self.assertIn('attack', outcome)