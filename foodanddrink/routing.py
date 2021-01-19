from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import restaurant.routing

application = ProtocolTypeRouter({
  # Empty for now (http->django views is added by default)
  'websocket': AuthMiddlewareStack(
      URLRouter(
          restaurant.routing.websocket_urlpatterns
      )
  ),
})
