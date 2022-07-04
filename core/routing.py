from channels.routing import ProtocolTypeRouter, URLRouter
from infrastructure.web.urls import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns)
})
