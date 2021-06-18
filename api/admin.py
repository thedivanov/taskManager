from django.contrib import admin
from .models import *

admin.site.register(Task_priority)
# admin.site.register(Task_status)
admin.site.register(Task)
admin.site.register(Employe)
admin.site.register(Responsible)
admin.site.register(Comment)
# admin.site.register(Notification)
admin.site.register(Notify_text)