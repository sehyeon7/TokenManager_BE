from django.db import models

from url.models import Url
from django.utils import timezone
# Create your models here.
class Request(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    type = models.CharField(max_length=8)
    requested_at = models.DateTimeField(default=timezone.now)



