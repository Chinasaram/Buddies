from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(
        max_length=200,
        null=True,
        unique=True,
        error_messages={"unique": "A user with this email already exists"},
    )
    username = models.CharField(
        max_length=200,
        null=True,
        unique=True,
        error_messages={"unique": "A user with this username already exists"},
    )
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="")

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants =
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
