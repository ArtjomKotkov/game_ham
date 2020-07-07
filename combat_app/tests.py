import json

from django.test import TestCase
from django.contrib.auth.models import User

from hero_app.services import Heroes
from .models import Combat, Field
from .combat import Combats
from .field import Fields
from .army import Stack, Army
from .units import Archer, ElFArcher

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

        hero1 = Heroes.objects.create_empty_hero(user=self.user1, hero_name='test_hero_user_1')
        hero2 = Heroes.objects.create_empty_hero(user=self.user2, hero_name='test_hero_user_1')
        hero1.army = army1
        hero1.save()
        hero2.army = army2
        hero2.save()

        basic_field = Fields('DF', 1).create('test_field')
        self.combat = Combats.create(name='test', field=basic_field)
        self.combat.add_hero_to_left_team(hero1)
        self.combat.add_hero_to_right_team(hero2)
        self.combat.start()

    def test_combat(self):
        import pprint
        pprint.pprint(self.combat.__dict__)

        pprint.pprint(self.combat.get_stack(0, 0).attack(self.combat.get_stack(1, 1)))
