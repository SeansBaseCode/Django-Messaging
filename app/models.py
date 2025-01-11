from django.db import models

from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

class Board(models.Model):
    topic = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    admin_username = models.CharField(max_length=100)
