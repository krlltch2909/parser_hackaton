from django.contrib import admin

# Register your models here.

from .models import EventTypeClissifier, Event


admin.site.register(EventTypeClissifier)
admin.site.register(Event)