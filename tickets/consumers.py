import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notifications'
        
        # Join notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave notification group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming WebSocket messages if needed
        pass

    async def ticket_notification(self, event):
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'ticket_notification',
            'message': event['message'],
            'ticket_id': event['ticket_id'],
            'action': event['action'],
            'timestamp': event.get('timestamp')
        }))