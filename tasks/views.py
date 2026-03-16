from rest_framework import generics

from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    ordering_fields = ["created_at", "status", "title"]
    ordering = ["-created_at"]
    search_fields = ["title", "description"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ["get", "patch", "delete"]
