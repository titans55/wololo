from channels.generic.websocket import WebsocketConsumer, AsyncConsumer, AsyncJsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.conf import settings
from .initFirestore import get_auth
auth = get_auth()
class ChatConsumer(WebsocketConsumer):
    def connect ( self ) :
        # Connects the channel named `self.channel_name`
        # to the group `jokes`
        print(self.channel_name)
        async_to_sync ( self. channel_layer . group_add ) (
            self.scope["session"]['userID'] , self. channel_name
        )
        # Accepts connection
        self. accept ( )
    def disconnect ( self, close_code ) :
        # Disables the channel named `self.channel_name`
        # from the group `jokes`
        async_to_sync ( self. channel_layer . group_discard ) (
            self.scope["session"]['userID'] , self. channel_name
        )
    # Method `notify_user` - event handler` notify.user`
    def notify_user ( self, event ) :
        # Sends a message on the web socket
        data = event['json']
        self. send ( text_data=json.dumps(data))