from django.contrib import admin

# Register your models here.

from .models import EventTypeClissifier, Event, Tag


admin.site.register(EventTypeClissifier)
admin.site.register(Event)
admin.site.register(Tag)