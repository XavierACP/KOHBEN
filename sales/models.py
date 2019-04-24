from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Person(models.Model):
    login = models.CharField(max_length=20, blank=False, default="")
    password = models.CharField(max_length=20, blank=False, default="")
    first_name = models.CharField(max_length=20, blank=False, default="")
    last_name = models.CharField(max_length=20, blank=False, default="")
    email = models.EmailField(max_length=30, default="@")
    avatar = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.first_name


class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(default="Nothing")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    myPhoto = models.ImageField(upload_to='static/img', default='blog-1.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
