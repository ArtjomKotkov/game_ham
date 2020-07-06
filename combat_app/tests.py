import json

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Combat, Field
from .services import Combats, Fields
from hero_app.services import Heroes
from army_app.services import Stack, Army
from army_app.units import Archer, ElFArcher


class TestCombat(TestCase):

    def setUp(self) -> None:
        army1 = {
            'Archer': 12,
            'ELFArcher': 6
        }
        army2 = {
            'Archer': 2,
            'ELFArcher': 9
        }
        self.user1 = User.objects.create_user('test_user1', password='123456')
        self.user2 = User.objects.create_user('test_user2', password='123456')

        hero1 = Heroes.objects.create_empty_hero(user=self.user1, hero_name='test_hero_user_1')
        hero2 = Heroes.objects.create_empty_hero(user=self.user2, hero_name='test_hero_user_1')


        basic_field = Fields('DF', 1).create('test_field')
        self.combat = Combats.create(name='test', field=basic_field)
        self.combat.add_hero_to_left_team(hero1)
        self.combat.add_hero_to_right_team(hero2)

        self.hero1 = Heroes.objects.load_hero(hero1)
        self.hero2 = Heroes.objects.load_hero(hero2)

        self.hero1.get_hero().army = army1
        self.hero1.get_hero().save()
        self.hero2.get_hero().army = army2
        self.hero2.get_hero().save()

        Army.load_army(self.hero1)
        Army.load_army(self.hero2)


    def test_combat(self):
        import pprint
        pprint.pprint(self.combat.__dict__)
