from django.urls import include, path,reverse_lazy
from rest_framework.routers import DefaultRouter
from tasks.views import TaskList, TaskCreate, TaskDetail, TaskUpdate,TaskDelete, CommentCreateView, CommentDeleteView


app_name='tasks'

urlpatterns = [
    path('', TaskList.as_view(), name='task-list'),
    path('tasks/create/', TaskCreate.as_view(), name='task-create'),
    path('tasks/<pk>/edit', TaskUpdate.as_view(), name='task-edit'),
    path('tasks/<pk>/delete', TaskDelete.as_view(), name='task-delete'),
    path('tasks/<pk>/detail', TaskDetail.as_view(), name='task-detail'),
    path('tasks/<int:pk>/comment',
        CommentCreateView.as_view(), name='task_comment_create'),
    path('tasks/comment/<int:pk>/delete',
        CommentDeleteView.as_view(), name='task_comment_delete')
]