import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.layers import get_channel_layer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("connecting...")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print("connected!")

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        ))

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['body_type']
        body = data['body']
        print(body)
        send_data = {
                'type': message_type,
                "body": body
        }
        # Send message to room group
        send = async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            send_data
        )
    # Receive message from room group
    def message(self, event):
        # Send message to WebSocket
        async_to_sync(self.send(text_data=json.dumps(event)))
    def announcement(self, event):
        async_to_sync(self.send(text_data=json.dumps(event)))



class UserConsumer(WebsocketConsumer):
    connected_users = []
    def connect(self):
        self.name = "foo"
        async_to_sync(self.channel_layer.group_add)(
            self.name,
            self.channel_name
        )
        UserConsumer.connected_users.append(self)
        self.accept()
    def disconnect(self, close_code):
        UserConsumer.connected_users.remove(self)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard(
            self.name,
            self.channel_name
        ))
    @staticmethod
    def get_user_updates(sender, instance, **kwargs):
        try:
            name = instance.first_name + " " + instance.last_name
            i = UserConsumer.connected_users[0]
            async_to_sync(i.channel_layer.group_send)(
                i.name, 
                {
                    "type": "message",
                    "message": name + " has registered for an account!"
                }
            )
        except: pass
    def message(self, event): async_to_sync(self.send(text_data=json.dumps(event["message"])))
