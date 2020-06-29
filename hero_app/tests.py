from django.test import TestCase
from django.contrib.auth.models import User

from .models import Hero
from .services import Heroes


class TestHeroes(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test', password='test2')

    def test_archer(self):
        archer = Heroes.Archer.create(self.user)
        archer_model = Hero.objects.get(user=self.user)
        self.assertEqual(archer.hero, archer_model)
        print(f'{archer.default_attack=}')
        self.assertEqual(archer.default_attack, archer_model.attack)

    def test_knight(self):
        knight = Heroes.Knight.create(self.user)
        knight_model = Hero.objects.get(user=self.user)
        self.assertEqual(knight.hero, knight_model)
        print(f'{knight.default_attack=}')
        self.assertEqual(knight.default_attack, knight_model.attack)

    def test_wizard(self):
        wizard = Heroes.Wizard.create(self.user)
        wizard_model = Hero.objects.get(user=self.user)
        self.assertEqual(wizard.hero, wizard_model)
        print(f'{wizard.default_attack=}')
        self.assertEqual(wizard.default_attack, wizard_model.attack)

class TestHeroesMethods(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test', password='test2')

    def test_atttack_changing(self):
        archer = Heroes.Archer.create(self.user)
        archer_model = Hero.objects.get(user=self.user)
        self.assertEqual(archer_model.attack, 14)
        archer.add_attack(12)
        archer_model = Hero.objects.get(user=self.user)
        self.assertEqual(archer_model.attack, 26)