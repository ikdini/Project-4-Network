from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  pass

class Post(models.Model):
  content = models.TextField()
  poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_post", null=True)
  created = models.DateTimeField(auto_now_add=True, null=True)
  likes = models.ManyToManyField(User, blank=True, related_name="liked")
