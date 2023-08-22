from django.contrib import admin

# Register your models here.
from example.models import *

class user_message_admin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'message', 'time')
admin.site.register(user_message, user_message_admin)