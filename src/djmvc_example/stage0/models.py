from django.db import models


class Stage0(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Stage0Tag(models.Model):
    stage = models.ForeignKey(Stage0, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
