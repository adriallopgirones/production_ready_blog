import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from core_apps.chat.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Endpoint for ws/chat/<other_user_id>/. When a user connects to this endpoint we create a room based
    on the user id and the user id of the user they want to talk with.
    We then create a room that will be used for real time communication between the two users.

    inspiration: https://dev.to/sirneij/backend-one-on-one-duologue-chatting-application-with-django-channels-and-sveltekit-1bim

    If we want to enable group chats at some point I think we'd only have to edit the room_name creation
    and handle n users instead of 2.
    """

    async def connect(self):
        """
        When a user opens a chat it establishes a websocket connection, therefore a group is created
        and added to the channel layer (redis db).
        """
        current_user_id = self.scope["user"].id
        other_user_id = int(self.scope["url_route"]["kwargs"]["other_user_id"])

        # Using numerical order to have a unique room name for both users independently of who is the sender
        self.room_name = (
            f"{current_user_id}_{other_user_id}"
            if current_user_id > other_user_id
            else f"{other_user_id}_{current_user_id}"
        )
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        When a user closes the chat it disconnects from the websocket and leaves the group.
        This should be done frequently to free up resources
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
        When a user sends a message it is received here and sent to the group aka the chat
        with the user whose id is the one in the request
        """
        data = json.loads(text_data)
        message = data["message"]

        # In the article they send the whole history of messages every time
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                # Above fields correspond to event argument in async def chat_message
                "message": message,
            },
        )

        await self.save_message(
            owner=self.scope["user"],
            message=message,
            room_group_name=self.room_group_name,
        )

    async def chat_message(self, event):
        """
        Used by channel_layer.group_send to send a message to the group
        """
        message = event["message"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, owner, message, room_group_name):
        Message.objects.create(
            owner=owner, message=message, room_group_name=room_group_name
        )
