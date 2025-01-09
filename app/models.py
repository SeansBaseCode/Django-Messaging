from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

class Board(models.Model):
    topic = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    admin_username = models.CharField(max_length=100)
