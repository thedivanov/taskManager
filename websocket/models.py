from django.db import models
from api.models import Employe

class Client(models.Model):
    channel_name = models.CharField('channel name', max_length=20)
