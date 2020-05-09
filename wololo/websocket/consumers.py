from channels.generic.websocket import WebsocketConsumer, AsyncConsumer, AsyncJsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.conf import settings
class ChatConsumer(WebsocketConsumer):
    def connect ( self ) :
        # Connects the channel named `self.channel_name`
        # to the group `jokes`
        if self.scope["user"].is_anonymous:
            raise Exception("Anonymous users not allowed")
        print(self.scope["user"].id)
        async_to_sync ( self. channel_layer . group_add ) (
            str(self.scope["user"].id) , self. channel_name
        )
        # Accepts connection
        self. accept ( )
    def disconnect ( self, close_code ) :
        # Disables the channel named `self.channel_name`
        # from the group `jokes`
        async_to_sync ( self. channel_layer . group_discard ) (
            str(self.scope["user"].id) , self. channel_name
        )
    # Method `notify_user` - event handler` notify.user`
    def notify_user ( self, event ) :
        # Sends a message on the web socket
        data = event['json']
        self. send ( text_data=json.dumps(data))