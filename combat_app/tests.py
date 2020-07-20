import pprint

from django.test import TestCase
from django.contrib.auth.models import User

from hero_app.models import Hero

from .combat.combat import Combats
from .combat.unit.basic import UNIT_CLASSES
from .combat.unit.logic import UnitAbstractClasses
from .combat.army import Stack


class TestCombat(TestCase):

    def setUp(self) -> None:
        self.army1 = {
            'Test': 100,
        }
        self.army2 = {unit: 20 for unit in UNIT_CLASSES if unit != 'Test'}

        self.user1 = User.objects.create_user('test_user1', password='123456')
        self.user2 = User.objects.create_user('test_user2', password='123456')

        hero1 = Hero.create(user=self.user1, hero_name='test_hero_user_1', hero_class='Knight', army=self.army1)
        hero2 = Hero.create(user=self.user2, hero_name='test_hero_user_2', hero_class='Demon', army=self.army2)

        self.combat = Combats.create(name='test', field='Simple')
        self.combat.combat.add_hero_to_left_team(hero1)
        self.combat.combat.add_hero_to_right_team(hero2)
        self.combat.start()
        self.combat.set_status_in_battle()