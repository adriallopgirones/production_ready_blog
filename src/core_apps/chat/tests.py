import asyncio

import pytest
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.urls import path

from core_apps.chat.consumers import ChatConsumer
from core_apps.chat.models import Message
from core_apps.users.factories import UserFactory

User = get_user_model()


async def get_messages(room_group_name):
    """
    Encapsulate all the DB operations here, it's a little messy because we need to transform
    every DB operation to sync.
    Notice that we return a plain Python object, because we'd get an error for using a DB object
    outside of the async context, when manipulating it in test.
    """
    msgs = await database_sync_to_async(Message.objects.filter)(
        room_group_name=room_group_name
    )
    msgs = await database_sync_to_async(msgs.values)(
        "owner", "message", "room_group_name"
    )

    msgs = await database_sync_to_async(list)(msgs)

    # Can't return anything related to a DB, or else we'll get an error when using it outside of this
    return msgs


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_chat_flow():
    # UserFactory involves db operations, so we need to use database_sync_to_async
    user1 = await database_sync_to_async(UserFactory)()
    user2 = await database_sync_to_async(UserFactory)()
    user3 = await database_sync_to_async(UserFactory)()

    # We create a URLRouter instead of passing ChatConsumer.as_asgi()to the communicator
    # because we need to pass the other_user_id as kwargs
    application = URLRouter(
        [
            path("ws/chat/<other_user_id>/", ChatConsumer.as_asgi()),
        ]
    )

    communicator_user1_user2 = WebsocketCommunicator(
        application, f"/ws/chat/{user2.id}/"
    )
    communicator_user2_user1 = WebsocketCommunicator(
        application, f"/ws/chat/{user1.id}/"
    )
    communicator_user3_user1 = WebsocketCommunicator(
        application, f"/ws/chat/{user1.id}/"
    )

    # AuthMiddlewareStack would set the scope in a real environment
    # There's not something like force_authentication in Channels, so we simulate it like:
    communicator_user1_user2.scope["user"] = user1
    communicator_user2_user1.scope["user"] = user2
    communicator_user3_user1.scope["user"] = user3

    # Connect User 1 to a chat room with User 2
    connected, _ = await communicator_user1_user2.connect()
    assert connected

    # Connect User 2 to a chat room with User 1
    connected, _ = await communicator_user2_user1.connect()
    assert connected

    # Connect User 3 to a chat room with User 1
    connected, _ = await communicator_user3_user1.connect()
    assert connected

    # User 1 sends a message to User 2
    message_from_user1 = {"message": "Hello User 2!"}
    await communicator_user1_user2.send_json_to(message_from_user1)

    # User 1 sends a second message to User 2
    message_from_user1_2 = {"message": "This is message 2"}
    await communicator_user1_user2.send_json_to(message_from_user1_2)

    # User 3 sends a message to User 1
    message_from_user3 = {"message": "Hello User 1!"}
    await communicator_user3_user1.send_json_to(message_from_user3)

    received_message_user2 = []
    while True:
        try:
            received_message_user2.append(
                await communicator_user2_user1.receive_json_from()
            )
            await asyncio.sleep(0.1)
        except Exception:
            break

    # Check if User 2 received the messages and that it hasn't received User 3's message
    assert len(received_message_user2) == 2
    assert received_message_user2[0]["message"] == message_from_user1["message"]
    assert received_message_user2[1]["message"] == message_from_user1_2["message"]

    # Check if Message models were created in the database
    messages_user1_user2 = await get_messages(f"chat_{user2.id}_{user1.id}")

    assert len(messages_user1_user2) == 2
    assert messages_user1_user2[0]["owner"] == user1.id
    assert messages_user1_user2[0]["message"] == message_from_user1["message"]
    assert messages_user1_user2[1]["owner"] == user1.id
    assert messages_user1_user2[1]["message"] == message_from_user1_2["message"]

    messages_user3_user1 = await get_messages(f"chat_{user3.id}_{user1.id}")

    assert len(messages_user3_user1) == 1
    assert messages_user3_user1[0]["owner"] == user3.id

    # Message created although User 1 never connected to that chat room
    assert messages_user3_user1[0]["message"] == message_from_user3["message"]

    # Clean up
    await communicator_user1_user2.disconnect()
    await communicator_user2_user1.disconnect()
    await communicator_user3_user1.disconnect()
