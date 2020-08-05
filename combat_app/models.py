import random

from django.db import models, Error
from django.core.validators import MinValueValidator, MaxValueValidator

from hero_app.models import Hero
from .combat.field import Fields

TYPES = (
    ('FR', 'Free'),
    ('EQ', 'Equal'),
    ('MG', 'MeatGrinder')
)

TYPES_COMBAT = (
    ('DF', 'TeamVsTeam'),
    ('MG', 'MeatGrinder')
)

COMBAT_STATUSES = [
    (None, 'None'),
    ('load', 'Loading'),
    ('prepare', 'Prepare'),
    ('inbattle', 'In Battle'),
    ('ended', 'Ended'),
]


class Combat(models.Model):
    name = models.CharField(max_length=80)
    datetime = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True)
    placement_time = models.IntegerField(validators=[MinValueValidator(3)])  # Minutes for connect players.
    placement_type = models.CharField(choices=TYPES, default='EQ', max_length=2)
    battle_type = models.CharField(choices=TYPES_COMBAT, default='DF', max_length=2)
    left_team = models.ManyToManyField(Hero, blank=True, related_name='lt')
    right_team = models.ManyToManyField(Hero, blank=True, related_name='rt')
    mg_team = models.ManyToManyField(Hero, blank=True, related_name='mgt')
    team_size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], default=1, null=True)
    field = models.CharField(max_length=30)
    status = models.CharField(max_length=8, null=True, blank=True, default=None, choices=COMBAT_STATUSES)

    def save(self, *args, **kwargs):
        if self.battle_type == 'DF' and self.team_size > 3:
            raise Error('In default battle type, team size can\'t be more then 3')
        if self.battle_type == 'MG' and self.team_size < 3:
            raise Error('In meat grinder battle type, team size can\'t be less then 3')
        check = Fields.check_field_is_aviable(self.battle_type, self.team_size, self.field)
        if check[0] == False:
            raise Error(check[1])
        return super().save(*args, **kwargs)

    def delete_hero_from_combat(self, hero):
        team = ''
        if hero in self.left_team.all():
            self.left_team.remove(hero)
            team = 'left'
        if hero in self.right_team.all():
            self.right_team.remove(hero)
            team = 'right'
        if hero in self.mg_team.all():
            self.mg_team.remove(hero)
            team = 'mg'
        print(team)
        hero.in_battle = -1
        hero.save(update_fields=['in_battle'])
        return team

    def add_hero_to_left_team(self, hero):
        assert self.battle_type == 'DF', 'Only default battle type provides left and right teams.'
        assert self.left_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self.left_team.add(hero)
        hero.in_battle = self.id
        hero.save(update_fields=['in_battle'])

    def add_hero_to_right_team(self, hero):
        assert self.battle_type == 'DF', 'Only default combat type provides left and right teams.'
        assert self.right_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self.right_team.add(hero)
        hero.in_battle = self.id
        hero.save(update_fields=['in_battle'])

    def add_hero_to_mg_team(self, hero):
        """
        Add user on MeatGrinder combat.
        :param user:
        :return:
        """
        assert self.battle_type == 'MG', 'Only MeatGrinder combat type provides this method.'
        assert self.mg_team.count() <= self.team_size, f'Size of team in this combat can\'t be more then {self.team_size}'
        self.mg_team.add(hero)
        hero.in_battle = self.id
        hero.save(update_fields=['in_battle'])

    def add_to_random_team(self, hero):
        if self.battle_type == 'MG':
            self.add_hero_to_mg_team(hero)
        else:
            if random.randrange(0, 1) == 0:
                self.add_hero_to_left_team(hero)
            else:
                self.add_hero_to_right_team(hero)

    def hero_in_combat(self, hero):
        if hero in self.left_team.all() or \
                hero in self.right_team.all() or \
                hero in self.mg_team.all():
            return True
        else:
            return False

    def set_status(self, status):
        assert status in (stts[0] for stts in COMBAT_STATUSES), 'Invalid combat status.'
        self.status = status
        self.save(update_fields=['status'])

    @property
    def is_started(self):
        statuses = [stts[0] for stts in COMBAT_STATUSES]
        statuses.remove(None)
        statuses.remove('ended')
        return True if self.status in statuses else False
