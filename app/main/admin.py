from django.contrib import admin

# Register your models here.

from .models import EventTypeClissifier, StatusOfEvent, Event

admin.site.register(StatusOfEvent)
admin.site.register(EventTypeClissifier)
admin.site.register(Event)