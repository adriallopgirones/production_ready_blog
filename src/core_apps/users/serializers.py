from rest_framework import serializers

from core_apps.users.models import PublicProfile


class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicProfile
        fields = "__all__"
        read_only_fields = ["owner"]
