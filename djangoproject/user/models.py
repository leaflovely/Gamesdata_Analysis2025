from django.db import models


class User(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
