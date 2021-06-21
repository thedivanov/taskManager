from logging import error
from api.models import Employe, Notify_text, Task
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Client

from asyncio import sleep

import json


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
            self.user_id = self.scope['url_route']['kwargs']['user_id']
            self.user_group_name = 'user_{}'.format(self.user_id)
            (self.channel_layer.group_add)(
                self.user_group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        (self.channel_layer.group_discard)(
            self.user_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        type = text_data_json['type']
        task_id = int(text_data_json['task_id'])

        task = self.get_task(task_id)
        user = self.get_user(self.user_id)

        if type == 'close.task':
            task.status = 'closed'
            self.update_task(task, 'status')

            if user.is_responsible:
                send_to = task.user_id.pk

            if not user.is_responsible:
                send_to = task.responsible_id.employe_id.pk

            print(self.channel_layer.group_send)

            (self.channel_layer.group_send)(
                'user_{}'.format(send_to),
                {
                    'type': 'close.task',
                    'message': task_id,
                    'task_id': task_id,
                })

        if type == 'start.task':
            task.status = 'open'

            self.update_task(task, 'status')


        if type == 'create.task':
            task.status = 'open'
            worker_id = text_data_json['worker_id']
            priority = text_data_json['priority']
            estab_time = text_data_json['estab_time']

            self.create_task(task_name=task.name, task_status=task.status, task_user_id=worker_id, established_time=estab_time, task_priority=priority)

            (self.channel_layer.group_send)(
                'user_{}'.format(worker_id),
                {
                    'type': 'create.task',
                    'message': task_id,
                    'task_id': task_id,
                })

        if type == 'delay.task':
            task.status = 'delayed'
            delay = text_data_json['delay_time']
            self.wait(delay)

            (self.channel_layer.group_send)(
                self.user_group_name,
                {
                    'type': 'delay.task',
                    'message': task_id,
                    'task_id': task_id,
                })



        # if type == 'open_task':
        #     task_user_id = text_data_json['task_user_id']
        #     task_name = text_data_json['task_name']
        #     task_text = text_data_json['task_text']
        #     task_priority = text_data_json['task_priority']
        #     task_established_time = text_data_json['task_established_time']

        #     self.create_task()

            # channel_message

        # if type == 'stop_task':
        #     await self.update_task(task, )

        # self.send(text_data=json.dumps({
        #     'type':event['type'],
        #     'message': event['message'],
        #     'user': event['user'],
        #     'status': event['status']
        # }))

        if type == 'update.worker':
            # send to old worker
            old_worker = self.get_task(task_id)
            (self.channel_layer.group_send)(
                'user_{}'.format(old_worker),
                {
                    'type': 'old.worker',
                    'message': task_id,
                    'task_id': task_id,
                })
            new_worker = text_data_json['new_worker']
            # send to new worker
            task.user_id = new_worker
            self.update_task(task, 'user_id')

            (self.channel_layer.group_send)(
                'user_{}'.format(new_worker),
                {
                    'type': 'new.worker',
                    'message': task_id,
                    'task_id': task_id,
                })

    def old_worker(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'event':'old.worker',
            'message':message
        }))

    def new_worker(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'event':'new.worker',
            'message':message
        }))

    def close_task(self, event):
        print('kek')
        message = event['message']

        self.send(text_data=json.dumps({
            'event':'close.task',
            'message':message
        }))

    def start_task(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'event':'start.task',
            'message':message
        }))

    def create_task(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'event':'create.task',
            'message':message
        }))

    def wait(self, delay, task_id):
        sleep(delay=delay)

        mess_text = self.get_message(1)
        (self.channel_layer.group_send)(
            self.task_group_name,
            {
                'type': 'delay.task.timeout',
                'message': task_id
            })


    # @database_sync_to_async
    def create_session(self, user_id):
        return Client.objects.create(channel_name=user_id)

    # @database_sync_to_async
    def get_message(self, message_id):
        return Notify_text.objects.get(pk=message_id)

    # @database_sync_to_async
    def get_session(self, user_id):
        return Client.objects.get(channel_name=user_id)

    # @database_sync_to_async
    def drop_session(self, user_id):
        return Client.objects.filter(channel_name=self.user_id).delete()

    # @database_sync_to_async
    def get_task(self, task_id):
        return Task.objects.get(pk=task_id)

    # @database_sync_to_async
    def get_task_user(self, task_id):
        return Task.objects.get(pk=task_id).user_id


    # @database_sync_to_async
    def get_user(self, user_id):
        user = User.objects.get(pk=user_id)
        return user.employe

    # @database_sync_to_async
    def update_task(self, task, update_field):
        return task.save(update_fields=['{}'.format(update_field)])

    # @database_sync_to_async
    def create_task(self, task_user_id, task_name, task_text, task_priority, task_established_time):
        Task.objects.create(user_id=task_user_id, name=task_name, text=task_text, priority=task_priority, established_time=task_established_time, responsible_id=self.user.id)
        Task.save()