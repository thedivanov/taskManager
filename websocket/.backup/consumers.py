from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
# from api.models import Notification, Notify_text

import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notificator_%s', self.room_name

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # notification = Notification.objects.get()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification',
                'message': message,
            }
        )

    async def send_notification(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'event': 'Send',
            'message': message
        }))