from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dictionary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=200)
    defination = models.TextField()

    def __str__(self):
        return f'{self.word}'
