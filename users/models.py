from django.db import models
from datetime import date

class User(models.Model) :
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    birth_date = models.DateField()
    user_email = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self) :
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['birth_date', 'first_name', 'last_name']

    @property
    def name(self) :
        return '{}  {}'.format(self.first_name, self.last_name)  

    @property
    def age(self) :
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month,self.birth_date.day))

