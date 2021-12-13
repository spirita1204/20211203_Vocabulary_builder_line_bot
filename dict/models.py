from django.db import models

# Create your models here.
class record(models.Model):
    Record_name = models.TextField()
    Record_content = models.TextField(default="")