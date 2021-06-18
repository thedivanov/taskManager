from django.http import response
from rest_framework import serializers
from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from api.models import Task, Task_status, Task_priority
from api.serializers import TasksSerializer

class TaskApiTestCase(APITestCase):
    def setUp(self):
        self.status_1 = Task_status.objects.create(task_status='open')
        self.priority_1 = Task_priority.objects.create(task_priority='critical')
        self.priority_2 = Task_priority.objects.create(task_priority='blocker')
        self.priority_3 = Task_priority.objects.create(task_priority='trivial')
        time = timezone.now()
        self.task_1 = Task.objects.create(task_name='Some task', task_text='Some text', priority=self.priority_1, status=self.status_1, task_date=time)
        self.task_2 = Task.objects.create(task_name='Another task', task_text='Some text', priority=self.priority_2, status=self.status_1, task_date=time)
        self.task_3 = Task.objects.create(task_name='Heare goes task', task_text='Lla', priority=self.priority_3, status=self.status_1, task_date=time)

    def test_get(self):
        url = reverse('task-list')
        response = self.client.get(url)
        serializer_data = TasksSerializer([self.task_1, self.task_2, self.task_3], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_search(self):
        url = reverse('task-list')
        response = self.client.get(url, data={'search': 'Some task'})
        serealized_data = TasksSerializer([self.task_1, self.task_2, self.task_3], many=True).data
        print(response)
        # self.assertEqual()

