# from django.shortcuts import render

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import asyncio


# from .models import Client


# getClinet = Client.objects.get()
def send_channel_message(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '{}'.format(group_name),
        {
            'type': 'update_task',
            'message': message
        }
    )

# from random import randint
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from django.http import HttpResponse

# channel_layer = get_channel_layer()

# def delay_task(request):
#     asyncio.sleep()
#     async_to_sync(channel_layer.send)('background-tasks', {'type': 'task_a', 'id': id})