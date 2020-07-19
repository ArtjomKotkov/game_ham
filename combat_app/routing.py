from django.urls import re_path, path

from .consumers import CombatsConsumer, CombatConsumer

websocket_urlpatterns = [
    re_path(r'ws/combats/', CombatsConsumer),
    path(r'ws/combat/<pk>', CombatConsumer),
]