from django.db import models


class Article(models.Model):
    question = models.TextField()
    answer = models.TextField()
    author = models.CharField(max_length=120)
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    publish_time = models.DateTimeField(auto_now_add=True)

