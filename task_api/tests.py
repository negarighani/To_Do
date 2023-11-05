from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task  
from tasks.serializers import TaskSerializer 

class TaskListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.tasks = []

        for i in range(3):
            task = Task.objects.create(owner=self.user, title='Test Task', description='This is a test task', status='T', priority='1')
            self.tasks.append(task)

    def test_list_tasks(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('api:tasks-list-create') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), len(self.tasks))

    def test_create_task(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'New Task',
            'description': 'This is a new task',
            'status': 'T',
            'priority': '1',
        }
        url = reverse('api:tasks-list-create')  
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get(title='New Task')
        self.assertEqual(task.title, 'New Task')
        self.assertEqual(task.description, 'This is a new task')
        self.assertEqual(task.status, 'T')
        self.assertEqual(task.priority, '1')
        self.assertEqual(task.owner, self.user)

class TaskDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'T',
            'priority': '1',
        }
        self.task = Task.objects.create(owner=self.user, **self.task_data)

    def test_get_task(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('api:tasks-get-edit-delete', args=[self.task.pk]) 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = TaskSerializer(self.task)
        self.assertEqual(response.data, serializer.data)

    def test_update_task(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Updated Task',
            'description': 'This is an updated task',
            'status': 'P',
            'priority': '2',
        }
        url = reverse('api:tasks-get-edit-delete', args=[self.task.pk]) 
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'This is an updated task')
        self.assertEqual(self.task.status, 'P')
        self.assertEqual(self.task.priority, '2')
        self.assertEqual(self.task.owner, self.user)

    def test_delete_task(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('api:tasks-get-edit-delete', args=[self.task.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Task.DoesNotExist):
            self.task.refresh_from_db()

