from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Message, Room, Topic, User

admin.site.register(User, UserAdmin)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
