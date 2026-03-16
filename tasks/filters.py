from django_filters import rest_framework as filters

from .models import Task


class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Task.Status.choices)
    created_by = filters.NumberFilter(field_name="created_by__id")
    assigned_to = filters.NumberFilter(field_name="assigned_to__id")

    class Meta:
        model = Task
        fields = ["status", "created_by", "assigned_to"]
