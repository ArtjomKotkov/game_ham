import json

from django.test import TestCase
from django.contrib.auth.models import User

from hero_app.models import Hero

from .combat.combat import Combats
from .combat.field import Fields
from .combat.hero import Heroes
from .combat.units import Archer, ElFArcher


class TestCombat(TestCase):

    def setUp(self) -> None:
        army1 = {
            'Archer': 12,
            'ELFArcher': 6
        }
        army2 = {
            'Archer': 15,
            'ELFArcher': 9
        }
        self.user1 = User.objects.create_user('test_user1', password='123456')
        self.user2 = User.objects.create_user('test_user2', password='123456')

        hero1 = Hero.create(user=self.user1, hero_name='test_hero_user_1', hero_class='Knight', army=army1)
        hero2 = Hero.create(user=self.user2, hero_name='test_hero_user_2', hero_class='Demon', army=army2)

        self.combat = Combats.create(name='test', field='simple')
        self.combat.add_hero_to_left_team(hero1)
        self.combat.add_hero_to_right_team(hero2)
        self.combat.start()

    def test_one(self):
        print(self.combat.field)