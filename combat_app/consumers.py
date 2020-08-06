import pprint
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from combat_app.combat.combat import Combats
from .models import Combat
from .serializers import CombatFullSerializer
from .combat.combat_manager import CombatManager
from .combat.handler.list_combat_handler import ListCombatHandler


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
                "data": ListCombatHandler().read(content, self.scope)
            },
        )

    def combat_list_message(self, event):
        print(event['data'])
        self.send_json(event['data'])



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





