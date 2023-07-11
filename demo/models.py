from django.db import models

# Create your models here.


class DynamicTable(models.Model):
    name = models.CharField("Name of dynamic table", max_length=30)

    def __str__(self):
        return self.name
