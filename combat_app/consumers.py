import json
import random
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from .serializers import CombatFullSerializer
from combat_app.combat.combat import Combats
from .models import Combat
from .serializers import CombatFullSerializer


class CombatsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        combats = Combat.objects.all()
        self.send_json({'basic': CombatFullSerializer(combats, many=True).data})
        async_to_sync(self.channel_layer.group_add)("combat_list", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("combat_list", self.channel_name)

    def receive_json(self, content, **kwargs):
        async_to_sync(self.channel_layer.group_send)(
            "combat_list",
            {
                "type": "combat_list.message",
                "data": self._handle(content),
            },
        )

    def combat_list_message(self, event):
        self.send_json(event['data'])

    def _handle(self, content):
        output = {}
        if 'create' in content:
            combat = Combats.create(
                name=f'test {random.randrange(1, 100000)}',
                field='Simple'
            )
            if 'created' in output:
                output['created'].append(CombatFullSerializer(combat).data)
            else:
                output['created'] = [CombatFullSerializer(combat).data]
            print(output)
        return output
