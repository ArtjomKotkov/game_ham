import pprint

from django.test import TestCase

from .basic import UNIT_CLASSES
from .logic import UnitAbstractClasses
from ..army import Stack


class TestsUnitBasic(TestCase):

    def setUp(self) -> None:
        self.test_unit = Stack(UNIT_CLASSES['Test'], 100, None)

    def test_temp_defense(self):
        self.test_unit.unit.add_temp_defense(3, 2)
        self.assertEqual(self.test_unit.unit.defense, 3)

        self.test_unit.unit.handle_turn()
        self.test_unit.unit.handle_turn()
        self.test_unit.unit.handle_turn()

        self.assertEqual(self.test_unit.unit.defense, 0)

    def test_temp_attack(self):
        attack = self.test_unit.unit.min_attack
        self.test_unit.unit.add_temp_attack(3, 2)


        self.assertEqual(self.test_unit.unit.min_attack, attack+3)

        self.test_unit.unit.handle_turn()
        self.test_unit.unit.handle_turn()
        self.test_unit.unit.handle_turn()

        self.assertEqual(self.test_unit.unit.min_attack, attack)

    def test_temp_initiative(self):
        init = self.test_unit.unit.initiative
        self.test_unit.unit.add_temp_initiative(3, 2)

        self.assertEqual(self.test_unit.unit.initiative, init+3)

        self.test_unit.unit.handle_turn()
        self.test_unit.unit.handle_turn()
        self.test_unit.unit.handle_turn()

        self.assertEqual(self.test_unit.unit.initiative, init)


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
    """
    UnitMeleeDoubleAttack is child of UnitMelee, therefore no tests for default answer and close / distance behavior.
    """

    def setUp(self) -> None:
        self.test_unit = Stack(UNIT_CLASSES['Test'], 100, None)
        self.modify = 'modify'
        self.answer_modify = 'answer'
        self.da_melee = Stack(UnitAbstractClasses.UnitMeleeDoubleAttack, 10, None)

    def test_double_attack(self):
        attack_output = self.da_melee.attack(self.test_unit)
        self.assertIn('enemy-double', attack_output)
        self.assertIn('enemy', attack_output)
        self.assertIn('self', attack_output)

    def test_double_attack_distance(self):
        self.da_melee.set_pos(10, 10)
        attack_output = self.da_melee.attack(self.test_unit)
        self.assertEqual(attack_output, {})


class TestsUnitDistanceDoubleAttack(TestCase):

    def setUp(self) -> None:
        self.test_unit = Stack(UNIT_CLASSES['Test'], 100, None)
        self.modify = 'modify'
        self.answer_modify = 'answer'
        self.da_distance = Stack(UnitAbstractClasses.UnitDistanceDoubleAttack, 10, None)

    def test_double_attack(self):
        self.da_distance.set_pos(10, 10)
        attack_output = self.da_distance.attack(self.test_unit)
        self.assertIn('enemy-double', attack_output)
        self.assertIn('enemy', attack_output)
        self.assertIn('self', attack_output)


class TestsUnitDistanceAnswer(TestCase):

    def setUp(self) -> None:
        self.test_unit = Stack(UNIT_CLASSES['Test'], 100, None)
        self.modify = 'modify'
        self.answer_modify = 'answer'
        self.a_distance = Stack(UnitAbstractClasses.UnitDistanceAnswer, 10, None)

    def test_answer_distance(self):
        self.a_distance.set_pos(10, 10)
        attack_output = self.test_unit.attack(self.a_distance)
        self.assertIn('self', attack_output)
        self.assertIn(self.modify, attack_output)


class TestsUnitUnlimitedAnswerMelee(TestCase):

    def setUp(self) -> None:
        self.test_unit = Stack(UNIT_CLASSES['Test'], 100, None)
        self.modify = 'modify'
        self.answer_modify = 'answer'
        self.a_melee = Stack(UnitAbstractClasses.UnitUnlimitedAnswerMelee, 10, None)

    def test_unlimited_answer(self):
        attack_output = self.a_melee.attack(self.test_unit)
        self.assertIn('self', attack_output)
        self.assertIn(self.modify, attack_output)
        self.assertIn(self.answer_modify, attack_output[self.modify])

        attack_output = self.a_melee.attack(self.test_unit)
        self.assertIn('self', attack_output)
        self.assertIn(self.modify, attack_output)
        self.assertIn(self.answer_modify, attack_output[self.modify])


class TestsUnitUnlimitedAnswerDistance(TestCase):

    def setUp(self) -> None:
        self.test_unit = Stack(UNIT_CLASSES['Test'], 100, None)
        self.modify = 'modify'
        self.answer_modify = 'answer'
        self.a_distance = Stack(UnitAbstractClasses.UnitUnlimitedAnswerDistance, 10, None)

    def test_unlimited_answer(self):
        self.a_distance.set_pos(10, 10)
        attack_output = self.a_distance.attack(self.test_unit)
        self.assertIn('self', attack_output)
        self.assertIn(self.modify, attack_output)
        self.assertIn(self.answer_modify, attack_output[self.modify])

        attack_output = self.a_distance.attack(self.test_unit)
        self.assertIn('self', attack_output)
        self.assertIn(self.modify, attack_output)
        self.assertIn(self.answer_modify, attack_output[self.modify])


