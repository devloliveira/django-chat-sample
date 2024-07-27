import json

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer


class ChatConsumer(SyncConsumer):
    """
    This class is responsible for handling the communication between client and server
    done within a websocket environment.

    In order to allow communication between two (or more) users within the same websocket,
    we create a channel layer and broadcast every message received to anyone connected
    to this group.

    Materials used: https://channels.readthedocs.io/en/
    """
    def websocket_connect(self, event):
        # Allows clients to establish a connection to the server via websocket.
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.send({'type': 'websocket.accept'})

    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        self.send({'type': 'websocket.disconnect'})

    def websocket_receive(self, event):
        print(f'Consumer received : {event}')
        contents = json.loads(event['text'])

        # Passes the message to the group synchronously
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": contents}
        )

    def chat_message(self, event):
        print(f'Chat message: {event}')
        message = event['message']['message']

        # Send message to WebSocket
        self.send({'type': 'websocket.send', 'text': message})