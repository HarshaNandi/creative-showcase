from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%Y-%m-%d %H:%M')}"
from django.db import models
from django.contrib.auth.models import User

class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"
