from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Url(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=512)

    def __str__(self):
        return self.url
    


