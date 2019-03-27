from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Person(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    mail = models.EmailField(max_length=30, default="@")
    avatar = models.CharField(max_length=200)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

