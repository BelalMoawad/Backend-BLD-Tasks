from django.db import models
from datetime import date


class Course(models.Model) :
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'description']

