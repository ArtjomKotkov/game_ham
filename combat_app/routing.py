from django.urls import re_path

from .consumers import CombatsConsumer

websocket_urlpatterns = [
    re_path(r'ws/combats/', CombatsConsumer),
]