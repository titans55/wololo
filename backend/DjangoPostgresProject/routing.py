from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from wololo.websocket.routing import websocket_urlpatterns
from channels.sessions import SessionMiddlewareStack
from wololo.websocket.websocket_jwt_auth import JWTAuthMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)

    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})