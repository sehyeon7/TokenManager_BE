from django.db import models
from request.models import Request
from django.utils import timezone

# Create your models here.
class Tokens(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField(default=timezone.now)
