from rest_framework import  status
from tasks.models import Task
from rest_framework.response import Response


def is_authorized(request, task):
    return request.user == task.owner

def get_task_object(pk):
        try:
            return Task.objects.get(pk=pk)
        except (ValueError,Task.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)