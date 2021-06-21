from typing import Match
from django.db import models
from django.db.models.deletion import CASCADE
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

class Task_priority(models.Model):
    BLOCKER = 'blocker'
    CRIT = 'critical'
    MAJOR = 'major'
    MEDIUM = 'medium'
    MINOR = 'minor'
    TRIVIAL = 'trivial'

    TASK_PRIORITY_CHOISES = (
        (BLOCKER, 'Blocker'),
        (CRIT, 'Critical'),
        (MAJOR, 'Major'),
        (MEDIUM, 'Medium'),
        (MINOR, 'Minor'),
        (TRIVIAL, 'Trivial'),
    )

    task_priority = models.CharField(max_length=10, choices=TASK_PRIORITY_CHOISES)
    priority = models.IntegerField()

    def __str__(self):
        return self.task_priority

class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_responsible = models.BooleanField('Является ли админом')

class Responsible(models.Model):
    employe_id = models.OneToOneField(Employe, on_delete=models.CASCADE)

    def __str___(self):
        return self.id

class Task(models.Model):
    CLOSED = 'closed'
    OPEN = 'open'
    ON_TEST = 'on_test'
    NEED_TO_MERGE = 'need_to_merge'
    DEVELOPING = 'developing'

    TASK_STATUS_CHOICES = (
        (CLOSED, 'Closed'),
        (OPEN, 'Open'),
        (ON_TEST, 'On test'),
        (NEED_TO_MERGE, 'Need to merge'),
        (DEVELOPING, 'Developing')
    )


    name = models.CharField('Название задачи', max_length=200)
    text = models.TextField('Текст задачи')
    priority = models.ForeignKey(Task_priority, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=TASK_STATUS_CHOICES, default=OPEN)
    user_id = models.OneToOneField(Employe, on_delete=models.PROTECT)
    responsible_id = models.ForeignKey(Responsible, on_delete=models.CASCADE)
    # start_date = models.DateTimeField('Дата постановки задачи', default=timezone.now())
    # established_time = models.DateTimeField('Оценочное время')
    # last_delta = models.DateTimeField('Оставшееся время', default=0)

class Comment(models.Model):
    employe_id = models.OneToOneField(Employe, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    date = models.DateTimeField('Дата комментария', default=timezone.now())

    def __str___(self):
        return self.text

class Notify_text(models.Model):
    text = models.TextField("Текст нотификации")

    def __str__(self):
        return self.text

