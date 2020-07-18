import pprint

from django.test import TestCase
from django.contrib.auth.models import User

from hero_app.models import Hero

from .combat.combat import Combats


class TestCombat(TestCase):

    def setUp(self) -> None:
        army1 = {
            'Archer': 12,
        }
        army2 = {
            'DemonArcher': 2,
            'Civilian': 10
        }
        self.user1 = User.objects.create_user('test_user1', password='123456')
        self.user2 = User.objects.create_user('test_user2', password='123456')

        hero1 = Hero.create(user=self.user1, hero_name='test_hero_user_1', hero_class='Knight', army=army1)
        hero2 = Hero.create(user=self.user2, hero_name='test_hero_user_2', hero_class='Demon', army=army2)

        self.combat = Combats.create(name='test', field='Simple')
        self.combat.combat.add_hero_to_left_team(hero1)
        self.combat.combat.add_hero_to_right_team(hero2)
        self.combat.start()

    def test_one(self):
        unit1 = self.combat.get_stack(0, 0)
        unit2 = self.combat.get_stack(1, 0)
        print(unit2.attack(unit1))
