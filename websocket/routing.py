from django.urls import re_path, path

from channels.routing import ProtocolTypeRouter, URLRouter

from .consumers import NotificationConsumer
# from .views import send_channel_message


websocket_urlpatterns = [
    re_path(r'ws/notify/(?P<user_id>\d+)/$', NotificationConsumer.as_asgi()),
]