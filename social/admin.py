from django.contrib import admin

from social.models import Messages, Room, Topic

# Register your models here.

admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Messages)