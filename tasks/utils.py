
from django.shortcuts import render
from rest_framework import  status
from tasks.models import Task
from rest_framework.response import Response

def custom_error_view(request, *args, **kwargs):
    context = {
        'message': 'You are trying to access to something that does not exist. Please click on Task Manager to get back to home page.',
    }
    return render(request, 'tasks/costume_error.html', context)

def get_task_object(pk):
        try:
            return Task.objects.get(pk=pk)
        except (ValueError,Task.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

def is_authorized(request, task):
    return request.user == task.owner

def get_authorization_error_context(request, task):
    if not is_authorized(request=request, task=task):
        return {'error': 'You are not authorized to perform this action. Please click on Task Manager to get back to home page.'}
    else:
        None
    
    