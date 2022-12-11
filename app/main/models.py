from datetime import datetime, timezone, timedelta
from dateutil.tz import tzlocal
from django.db import models

# Create your models here.


class EventTypeClissifier(models.Model):
    """
    классификатор типов события
    """
    type_code = models.SmallAutoField(primary_key=True,
                                      verbose_name="type_code")
    description = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.description

    def __hash__(self) -> int:
        return id(self)


class HistoryUserRequest(models.Model):
    """
    модель для записей о времени обращения конкретного пользователя к серверу
    """

    user_id = models.IntegerField(primary_key=True)
    time_of_last_request = models.DateTimeField(auto_now=True)

    def __str__(self) -> int:
        return self.user_id


class Tag(models.Model):
    """
    классификатор тегов
    """
    tag_code = models.SmallAutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.description


class Keyword(models.Model):
    """
    ключевое слово для тега
    """
    keyword_code = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=255)
    tag_code = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.content


class Event(models.Model):
    """
    модель всех событий
    """
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    address = models.CharField(max_length=255, blank=True, null=True)

    start_date = models.DateTimeField(blank=True, null=True)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    url = models.URLField(max_length=255)

    type_of_event = models.ForeignKey(EventTypeClissifier,
                                      on_delete=models.CASCADE)
    is_free = models.BooleanField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)

    date_of_parsing = models.DateTimeField(auto_now_add=True)
    
    def already_exists(self) -> bool:
        saved_events = Event.objects.all()
        for saved_event in saved_events:
            new_event_title = self.title.lower().strip()
            saved_event_title = saved_event.title.lower().strip()
            if new_event_title == saved_event_title:
                return True
        return False
    
    def is_expired(self) -> bool:
        moscow_tz = timezone(timedelta(hours=3))
        today = datetime.now(tzlocal()).astimezone(moscow_tz)
        if self.registration_deadline is not None \
            and self.registration_deadline < today:
                return True
        if self.end_date is not None \
            and self.end_date < today:
                return True
        return False

    def __str__(self) -> str:
        return self.title

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Event):
            return self.title == __o.title
        return False

    def __hash__(self) -> int:
        return id(self)
