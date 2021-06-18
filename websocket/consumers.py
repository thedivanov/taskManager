from channels.consumer import SyncConsumer
from api.models import Employe, Notify_text, Task
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync

from .models import Client

from asyncio import sleep

import json
import datetime


class NotificationConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = 'task_{}'.format(self.task_id)
        await (self.channel_layer.group_add)(
            self.task_group_name,
            self.channel_name
        )
        # self.create_session(self.user_id)

        self.accept()

    async def disconnect(self, close_code):
        await (self.channel_layer.group_discard)(
            self.task_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        type = text_data_json['type']
        task_id = int(text_data_json['task_id'])
        user_id = text_data_json['user_id']

        task = await self.get_task(task_id)
        user = await self.get_user(user_id)

        if type == 'close_task':
            task.status = 'closed'
            self.update_task(task, 'status')

            await(self.channel_layer.group_send)(
                self.task_group_name,
                {
                    'type': 'close_task',
                    'message': task_id
                })

            # if not user.is_responsible:
            #     send_to = task.responsible_id
                # await self.send(
                #     self.send_to,
                #     {
                #         'type':'close_task',
                #         'message':''
                #     }
                # )

        if type == 'start_task':
            task.status = 'open'
            worker_id = text_data_json['worker_id']
            priority = text_data_json['priority']
            estab_time = text_data_json['estab_time']

            await self.create_task(name=user_id, status=task.status, user_id=worker_id, established_time=estab_time)


        if type == 'create_task':
            task.status = 'open'
            worker_id = text_data_json['worker_id']
            priority = text_data_json['priority']
            estab_time = text_data_json['estab_time']

            await self.create_task(name=user_id, status=task.status, user_id=worker_id, established_time=estab_time)

            await (self.channel_layer.group_send)(
                self.task_group_name,
                {
                    'type': 'create_task',
                    'message': task_id,
                })

        if type == 'delay_task':
            task.status = 'delayed'
            delay = text_data_json['delay_time']
            self.wait(delay)

            await (self.channel_layer.group_send)(
                self.task_group_name,
                {
                    'type': 'delay_task',
                    'message': task_id,
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

        if type == 'update_worker':
            old_worker = await self.get_task(task_id)
            await (self.channel_layer.group_send)(
                self.task_group_name,
                {
                    'type': 'old_worker',
                    'message': task_id,
                })
            # send to old worker
            new_worker = text_data_json['new_worker']
            # send to new worker
            task.user_id = new_worker
            self.update_task(task, 'user_id')

            await (self.channel_layer.group_send)(
                self.task_group_name,
                {
                    'type': 'new_worker',
                    'message': task_id,
                })

    async def old_worker(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'event':'old_worker',
            'message':message
        }))

    async def new_worker(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'event':'new_worker',
            'message':message
        }))

    async def close_task(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'event':'close_task',
            'message':message
        }))

    async def start_task(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'event':'start_task',
            'message':message
        }))

    async def create_task(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'event':'create_task',
            'message':message
        }))

    async def wait(self, delay, task_id):
        sleep(delay=delay)

        mess_text = await self.get_message(1)
        await (self.channel_layer.group_send)(
            self.task_group_name,
            {
                'type': 'delay_task_timeout',
                'message': task_id
            })


    @database_sync_to_async
    def create_session(self, user_id):
        return Client.objects.create(channel_name=user_id)

    @database_sync_to_async
    def get_message(self, message_id):
        return Notify_text.objects.get(pk=message_id)

    @database_sync_to_async
    def get_session(self, user_id):
        return Client.objects.get(channel_name=user_id)

    @database_sync_to_async
    def drop_session(self, user_id):
        return Client.objects.filter(channel_name=self.user_id).delete()

    @database_sync_to_async
    def get_task(self, task_id):
        return Task.objects.get(pk=task_id)

    @database_sync_to_async
    def get_task_user(self, task_id):
        return Task.objects.get(pk=task_id).user_id


    @database_sync_to_async
    def get_user(self, user_id):
        user = User.objects.get(pk=user_id)
        return user.employe

    @database_sync_to_async
    def update_task(self, task, update_field):
        return task.save(update_fields=['{}'.format(update_field)])

    @database_sync_to_async
    def create_task(self, task_user_id, task_name, task_text, task_priority, task_established_time):
        Task.objects.create(user_id=task_user_id, name=task_name, text=task_text, priority=task_priority, established_time=task_established_time, responsible_id=self.user.id)
        Task.save()