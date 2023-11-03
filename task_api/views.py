from rest_framework import  status
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from task_api.utils import is_authorized, get_task_object


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):

    if request.method == 'GET':
        
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            task = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    
    task=get_task_object(pk)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not is_authorized:
            return Response({'message': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(task, request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not is_authorized:
            return Response({'message': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
