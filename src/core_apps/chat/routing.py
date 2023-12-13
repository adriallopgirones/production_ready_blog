from django.urls import re_path

from core_apps.chat import consumers

websocket_urlpatterns = [
    # re_path allows to define variable names that can be passed to the consumer
    # $ ignores anything after the variable
    re_path(r"ws/chat/<other_user_id>/$", consumers.ChatConsumer.as_asgi()),
]
