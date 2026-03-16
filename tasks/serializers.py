from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_by",
            "assigned_to",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
