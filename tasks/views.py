import copy
from django.forms import ValidationError
from django.urls import reverse
from tasks.models import Comment, Task
from rest_framework import  status
from django.shortcuts import redirect
from tasks.models import Task
from tasks.serializers import CommentSerializer, TaskSerializer, TaskSerializerWithoutOwner
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from tasks.owner import  OwnerDeleteView, OwnerUpdateView, OwnerView, OwnerDetailView, OwnerCreate, OwnerList
from django.db.models import Q
from tasks.utils import get_authorization_error_context, get_task_object, is_authorized

class TaskList(OwnerList):
    serializer_class = TaskSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_list.html'
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        strval =  request.GET.get("search", False)
        if strval :
            query = Q(title__icontains=strval) 
            query.add(Q(description__icontains=strval), Q.OR)

            tasks = Task.objects.filter(query).select_related().order_by('priority')
        else:
            tasks = Task.objects.all().order_by('priority')
            
        context = {
            'tasks': tasks,
            'strval':strval,
        }
        return Response(context)


class TaskCreate(OwnerCreate):
    serializer_class = TaskSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_create.html'
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = TaskSerializerWithoutOwner()
        context = {
            
            'serializer': serializer,
        }
        return Response(context)
    
    def post(self, request):
        serializer = TaskSerializerWithoutOwner(data=request.POST, context={'request': request})
        if not serializer.is_valid():
            tasks = Task.objects.all()
            context = {
            'tasks': tasks,
            'serializer': serializer,
            }
            return Response(context)

        task = serializer.save()
        return redirect(reverse('tasks:task-list'))

class TaskDetail(OwnerDetailView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_detail.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task=get_task_object(pk)
        comments = Comment.objects.filter(task=task)
        context = {
            'task': task,
            'comments' : comments,
            
        }
        return Response(context)


class TaskDelete(OwnerView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_confirm_delete.html'
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        task=get_task_object(pk)
        if request.user != task.owner:
            context= {
                'error':'You are not authorized to perform this action. Please click on Task Manager to get back to home page.'
            }
        else:
            context = {
                'task': task,
            }
        return Response(context)
    
    def delete(self, request, pk):
        task = get_task_object(pk)
        if request.user != task.owner:
            context= {
                'error':'You are not authorized to perform this action. Please click on Task Manager to get back to home page.'
            }
            return Response(context)
        else:
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TaskUpdate(OwnerUpdateView):
    serializer_class = TaskSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/task_form.html'
    permission_classes = [IsAuthenticated]
    task_statuses=Task._meta.get_field('status').choices
    task_priorities=Task._meta.get_field('priority').choices
    
    def get(self, request, pk):
        task=get_task_object(pk)
        context= get_authorization_error_context(request, task)
        if context is None:
            context = {
            'task': task,
            'task_statuses':self.task_statuses,
            'task_priorities':self.task_priorities
        }
        return Response(context)

    def post(self, request, pk):
        task=get_task_object(pk)
        context= get_authorization_error_context(request, task)
        if context is None:
            serializer = TaskSerializerWithoutOwner(data=request.POST,context={'request': request})
            if not serializer.is_valid():
                context = {
                    'task': task,
                    'serializer_error': serializer.errors,
                    'task_statuses':self.task_statuses,
                    'task_priorities':self.task_priorities
                }
                return Response(context)
        
        data = copy.deepcopy(request.POST)
        if data['due_date'] == '':
            data['due_date'] = None
        serializer.update(task, data)
        task.save()
        return redirect(reverse('tasks:task-list'))

class CommentCreateView(OwnerCreate):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk) :
        task=get_task_object(pk)
        serializer = CommentSerializer(data=request.POST)
        if not serializer.is_valid:
            redirect(reverse('tasks:task-detail', args=[pk]))
            
        comment = Comment(text=request.POST.get('text'), writer=request.user, task=task)
        comment.save()
        return redirect(reverse('tasks:task-detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            if  is_authorized:
                comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except (ValueError,Task.DoesNotExist, Exception):
                return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

