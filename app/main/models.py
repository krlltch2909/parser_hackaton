from django.db import models


# Create your models here.


# классификатор типов события
class EventTypeClissifier(models.Model):
    type_code = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class EventCostClassifier(models.Model):
    cost_code = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Tags(models.Model):
    tage_code = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    address = models.CharField(max_length=255, blank=True, null=True)

    start_date = models.DateTimeField(blank=True, null=True)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True,  null=True)

    url = models.URLField(max_length=255)
    img = models.URLField(max_length=255, null=True)

    type_of_event = models.ForeignKey(EventTypeClissifier, on_delete=models.DO_NOTHING)
    event_cost_type = models.ForeignKey(EventCostClassifier, on_delete=models.DO_NOTHING, null=True, blank=True)

    tag = models.ManyToManyField(Tags, blank=True, null=True)

    def __str__(self):
        return self.title

    # def __str__(self):
    #     return self.title + " " + self.url


