from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound

from core_apps.chat.models import Message
from core_apps.chat.serializers import MessageSerializer
from core_apps.common.permissions import IsOwnerOrReadOnly


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        room_group_name = self.request.query_params.get("room_group_name", None)

        if not room_group_name:
            raise NotFound("room_group_name parameter is required.")

        queryset = Message.objects.filter(room_group_name=room_group_name)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
