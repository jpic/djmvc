from django.db import models


class Stage0Model(models.Model):
    name = models.CharField(max_length=100)
