from django.test import TestCase

from .basic import UNIT_CLASSES
from .logic import UnitAbstractClasses
from ..army import Stack


class TestsUnitBasic(TestCase):
    pass


class TestsUnitMelee(TestCase):

    def setUp(self) -> None:
        self.test_unit = Stack(UNIT_CLASSES['Test'], 100, None)
        self.modify = 'modify'
        self.answer_modify = 'answer'
        self.melee_unit = Stack(UnitAbstractClasses.UnitMelee, 10, None)

    def test_melee_unit_answer_close(self):
        """
        Testing that MeleeUnit have only 1 answer.
        """
        attack_output = self.test_unit.attack(self.melee_unit)
        self.assertIn(self.modify, attack_output)
        self.assertIn(self.answer_modify, attack_output[self.modify])

        second_attack_output = self.test_unit.attack(self.melee_unit)
        self.assertNotIn(self.modify, second_attack_output)

    def test_melee_unit_answer_distance(self):
        self.melee_unit.set_pos(10, 10)
        attack_output = self.test_unit.attack(self.melee_unit)
        self.assertNotIn('self', attack_output)

    def test_melee_unit_attack_close(self):
        attack_output = self.melee_unit.attack(self.test_unit)
        self.assertIn('enemy', attack_output)

    def test_melee_unit_attack(self):
        self.melee_unit.set_pos(10, 10)
        attack_output = self.melee_unit.attack(self.test_unit)
        self.assertEqual(attack_output, {})


class TestsUnitDistanse(TestCase):

    def setUp(self) -> None:
        self.test_unit = Stack(UNIT_CLASSES['Test'], 100, None)
        self.modify = 'modify'
        self.answer_modify = 'answer'
        self.distance_unit = Stack(UnitAbstractClasses.UnitDistanse, 10, None)

    def test_distance_unit_answer_close(self):
        """
        Testing that MeleeUnit have only 1 answer.
        """
        # If units are close.
        attack_output = self.test_unit.attack(self.distance_unit)
        self.assertIn(self.modify, attack_output)
        self.assertIn(self.answer_modify, attack_output[self.modify])

    def test_distance_unit_answer(self):
        self.distance_unit.set_pos(10, 10)
        attack_output = self.test_unit.attack(self.distance_unit)
        self.assertNotIn(self.modify, attack_output)

    def test_distance_unit_attack(self):
        self.distance_unit.set_pos(10, 10)
        attack_output = self.distance_unit.attack(self.test_unit)
        self.assertIn('enemy', attack_output)


class TestsUnitMeleeDoubleAttack(TestCase):
    pass


class TestsUnitDistanceDoubleAttack(TestCase):
    pass


class TestsUnitDistanceAnswer(TestCase):
    pass


class TestsUnitUnlimitedAnswerMelee(TestCase):
    pass


class TestsUnitUnlimitedAnswerDistance(TestCase):
    pass