from django.db import models


class Stage0(models.Model):
    name = models.CharField(max_length=100)
