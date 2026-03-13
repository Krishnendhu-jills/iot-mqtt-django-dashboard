from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/temperature/", consumers.TemperatureConsumer.as_asgi()),
]