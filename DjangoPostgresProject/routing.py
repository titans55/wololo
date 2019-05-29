from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import wololo.routing
from wololo.consumers import ChatConsumer
from channels.sessions import SessionMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)

    'websocket': SessionMiddlewareStack(
        URLRouter(
            wololo.routing.websocket_urlpatterns
        )
    ),
})