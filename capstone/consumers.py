import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            message = text_data_json['message']
            ok = "message"
        except KeyError:
            message = text_data_json["annoucement"]
            ok = "annoucement"
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'announcement',
                ok: message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        try:
            message = event['message']
        except KeyError:
            message = event['annoucement']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # receive announcement from class   
    async def announcement(self, event):
        try:
            message = event["annoucement"]
            ok = "annoucement"
        except KeyError:
            message = event["message"]
            ok = "message"

        await self.send(text_data=json.dumps({
            ok: message
        }))
