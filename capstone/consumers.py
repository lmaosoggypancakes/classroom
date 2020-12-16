import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await (self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        ))
        print("connected!")
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect rip")
        # Leave room group
        (self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        ))

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        try:
            message = text_data_json['message']
            ok = "message"
        except KeyError:
            message = text_data_json["annoucement"]
            ok = "annoucement"
        # Send message to room group
        await (self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'announcement',
                ok: message
            }
        ))

    # Receive message from room group
    async def chat_message(self, event):
        print("Event: ", event)
        try:
            message = event['message']
        except KeyError:
            message = event['annoucement']
        # Send message to WebSocket
        (self.send(text_data=json.dumps({
            'message': message
        })))

    # receive announcement from class   
    async def announcement(self, event):
        try:
            message = event["annoucement"]
            ok = "annoucement"
        except KeyError:
            message = event["message"]
            ok = "message"

        (self.send(text_data=json.dumps({
            ok: message
        })))
