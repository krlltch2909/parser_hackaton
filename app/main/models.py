from django.db import models


# Create your models here.

# классификатор типов события
class EventTypeClissifier(models.Model):
    type_code = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


# классификатор статуса события
class StatusOfEvent(models.Model):
    status_code = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    address = models.CharField(max_length=255, blank=True)

    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    url = models.CharField(max_length=255)

    type_of_event = models.ForeignKey(EventTypeClissifier, on_delete=models.DO_NOTHING)
    status_of_event = models.ForeignKey(StatusOfEvent, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
