from django.db import models
from django.contrib.auth.models import User

class my_user(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, unique=True)
    salary = models.FloatField(default=0)
    percentage = models.FloatField(default=0)

    def __str__(self):
        return self.name
