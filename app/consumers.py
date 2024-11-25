# app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PlacarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("placar", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("placar", self.channel_name)

    async def match_update(self, event):
        print("ja disse?")
        match_data = event['match']
        await self.send(text_data=json.dumps(match_data))
