from sys import maxsize
from django.db import models

class Course(models.Model) :
    # course_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)

    def __str__(self):
        return self.name     
