from django.urls import path
from task_api.views import task_detail, task_list


app_name='api'

urlpatterns = [
    path('tasks/', task_list, name='tasks-list-create'),
    path('tasks/<pk>/', task_detail, name='tasks-get-edit-delete')
]