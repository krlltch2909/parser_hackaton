from django.db import models

# Create your models here.

class Title(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
