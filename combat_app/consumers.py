import pprint
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.urls import reverse

from .serializers import CombatFullSerializer
from combat_app.combat.combat import Combats
from hero_app.models import Hero
from .models import Combat
from .serializers import CombatFullSerializer
from .combat.combat_manager import CombatManager


class CombatsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        combats = Combat.objects.filter(status=None).order_by('battle_type')
        self.send_json({'basic': CombatFullSerializer(combats, many=True).data})
        async_to_sync(self.channel_layer.group_add)("combat_list", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("combat_list", self.channel_name)

    def receive_json(self, content, **kwargs):
        print(content)
        async_to_sync(self.channel_layer.group_send)(
            "combat_list",
            {
                "type": "combat_list.message",
                "data": self._handle(content),
            },
        )

    def combat_list_message(self, event):
        print(event['data'])
        self.send_json(event['data'])

    def _handle(self, content):
        output = {}
        errors_output = {}
        if 'create' in content:
            data = content['create']
            combat = Combats.create(
                name=data['name'],
                placement_time=int(data['placement_time']),
                placement_type=data['placement_type'],
                battle_type=data['battle_type'],
                team_size=int(data['team_size']),
                field=data['field'],
            )

            combat.add_to_random_team(self.scope["user"].heroapp.selected_hero)
            output.setdefault('created', {}).update({
                'combat': CombatFullSerializer(combat).data,
                'hero_id': self.scope["user"].heroapp.selected_hero.id
            })

        if 'exit' in content:
            data = content['exit']
            try:
                combat = Combat.objects.get(id=data.get('combat_id', -1))
            except Combat.DoesNotExist:
                return errors_output.setdefault('exit', {}).update({
                    'status': False,
                    'error': 'Combat does not exist, or combat_id doesn\'t provided.'
                })
            try:
                hero = Hero.objects.get(id=data.get('hero_id', -1))
            except Hero.DoesNotExist:
                return errors_output.setdefault('exit', {}).update({
                    'status': False,
                    'error': 'Hero does not exist, or hero_id doesn\'t provided.'
                })
            team = combat.delete_hero_from_combat(hero)
            output.setdefault('exit', {}).update({
                'status': True,
                'team': team,
                'combat_index': data['combat_index'],
                'hero_id': data['hero_id']
            })

        if 'connect' in content:
            data = content['connect']
            if not 'team' in data:
                return errors_output.setdefault('connect', {}).update({
                    'status': False,
                    'error': 'Team doesn\'t provided.'
                })
            if not 'combat_id' in data:
                return errors_output.setdefault('connect', {}).update({
                    'status': False,
                    'error': 'Combat_id doesn\'t provided.'
                })
            if not 'hero_id' in data:
                return errors_output.setdefault('connect', {}).update({
                    'status': False,
                    'error': 'Hero_id doesn\'t provided.'
                })
            if not 'combat_index' in data:
                return errors_output.setdefault('connect', {}).update({
                    'status': False,
                    'error': 'Combat_index doesn\'t provided.'
                })
            try:
                combat = Combat.objects.get(id=data.get('combat_id', -1))
            except Combat.DoesNotExist:
                return errors_output.setdefault('exit', {}).update({
                    'status': False,
                    'error': 'Combat does not exist, or combat_id doesn\'t provided.'
                })
            try:
                hero = Hero.objects.get(id=data.get('hero_id', -1))
            except Hero.DoesNotExist:
                return errors_output.setdefault('exit', {}).update({
                    'status': False,
                    'error': 'Hero does not exist, or hero_id doesn\'t provided.'
                })
            if combat.hero_in_combat():
                return
            if data['team'] == 'left':
                combat.add_hero_to_left_team(hero)
                output.setdefault('connect', {}).update({
                    'team': 'left',
                })
            elif data['team'] == 'right':
                combat.add_hero_to_right_team(hero)
                output.setdefault('connect', {}).update({
                    'team': 'right',
                })
            else:
                combat.add_hero_to_mg_team(hero)
                output.setdefault('connect', {}).update({
                    'team': 'mg',
                })

            output.setdefault('connect', {}).update({
                'status': True,
                'combat_index': data['combat_index'],
                'hero_id': hero.id,
                'hero_name': hero.name,
                'hero_url': reverse('user:user_page', args=[hero.user.username]),
                'combat_id': data.get('combat_id', -1)
            })
        return output


class CombatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        combat = Combat.objects.get(pk=int(self.scope['url_route']['kwargs']['pk']))

        async_to_sync(self.channel_layer.group_add)(f'combat_{self.scope["url_route"]["kwargs"]["pk"]}',
                                                    self.channel_name)

        combat_inst = Combats(combat)
        CombatManager().add_combat(combat_inst)

    def combat_message(self, message):
        pprint.pprint(message)
        self.send_json(message)

    def all_combat_message(self, event):
        pprint.pprint(event['data'])
        self.send_json(event['data'])

    def group_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            f'combat_{self.scope["url_route"]["kwargs"]["pk"]}',
            {
                "type": "all_combat.message",
                "data": message
            },
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(f'combat_{self.scope["url_route"]["kwargs"]["pk"]}',
                                                        self.channel_name)

    def receive_json(self, content, **kwargs):
        if 'command' in content:
            if content['command'] == 'load_battle':
                pk = int(self.scope["url_route"]["kwargs"]["pk"])
                combat = CombatManager().get_combat(pk)
                self.group_message(combat.combat_info())





