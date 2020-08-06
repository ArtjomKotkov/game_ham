from django.shortcuts import get_object_or_404, reverse

from hero_app.models import Hero
from .incombat_handler import func_name_adder
from ..combat import Combats
from ...serializers import CombatFullSerializer
from ...models import Combat


class ListCombatHandler:

    def __init__(self):
        self.outcome = {}

    def read(self, content, scope):

        self.scope = scope

        if 'create' in content:
            self.create(content['create'])

        if 'exit' in content:
            self.exit(content['exit'])

        if 'connect' in content:
            self.connect(content['connect'])

        return self.outcome

    @func_name_adder
    def create(self, content):
        """Create new combat and connect user which created its."""
        validation_list = ['name', 'placement_time', 'placement_type', 'battle_type', 'team_size', 'field']
        assert all(elem in content for elem in validation_list),\
            'Invalid request, required fields: name, placement_time, placement_type, battle_type, team_size, field'

        combat = Combats.create(
            name=content['name'],
            placement_time=int(content['placement_time']),
            placement_type=content['placement_type'],
            battle_type=content['battle_type'],
            team_size=int(content['team_size']),
            field=content['field'],
        )

        team = combat.combat.add_to_random_team(self.scope["user"].heroapp.selected_hero)

        hero = self.scope["user"].heroapp.selected_hero

        return {
            'combat': CombatFullSerializer(combat.combat).data,
            'hero_id': hero.id,
            'hero_name': hero.name,
            'hero_url': reverse('user:user_page', args=[hero.user.username]),
            'combat_id': combat.combat.id,
            'team': team
        }

    @func_name_adder
    def exit(self, content):
        """Delete hero from combat."""

        validation_list = ['combat_id', 'hero_id']
        assert all(elem in content for elem in validation_list),\
            'Invalid request, required fields: combat_id, hero_id'
        combat = get_object_or_404(Combat, id=content.get('combat_id', -1))
        hero = get_object_or_404(Hero, id=content.get('hero_id', -1))

        team = combat.delete_hero_from_combat(hero)
        return {
            'team': team,
            'combat_index': content['combat_index'],
            'hero_id': content['hero_id']
        }

    @func_name_adder
    def connect(self, content):
        """Connect hero to team."""


        validation_list = ['team', 'combat_id', 'combat_id', 'hero_id', 'combat_index']
        assert all(elem in content for elem in validation_list), \
            'Invalid request, required fields: team, combat_id, combat_id, hero_id, combat_index'

        combat = get_object_or_404(Combat, id=content.get('combat_id', -1))
        hero = get_object_or_404(Hero, id=content.get('hero_id', -1))

        assert combat.hero_in_combat(hero) == False, 'Hero already in combat.'

        output = {
            'combat_index': content['combat_index'],
            'hero_id': hero.id,
            'hero_name': hero.name,
            'hero_url': reverse('user:user_page', args=[hero.user.username]),
            'combat_id': content.get('combat_id', -1)
        }

        if content['team'] == 'left':
            combat.add_hero_to_left_team(hero)
        elif content['team'] == 'right':
            combat.add_hero_to_right_team(hero)
        elif content['team'] == 'mg':
            combat.add_hero_to_mg_team(hero)

        output.update({
            'team': content['team'],
        })

        return output
