import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlertConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Add this connection to the "alerts" group
        await self.channel_layer.group_add(
            "alerts",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove connection from alerts group
        await self.channel_layer.group_discard(
            "alerts",
            self.channel_name
        )

    async def send_alert(self, event):
        message = event["message"]

        # Send alert message to browser
        await self.send(text_data=json.dumps({
            "message": message
        }))