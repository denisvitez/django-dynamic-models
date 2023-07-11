from django.db import models

# Create your models here.


class DynamicTable(models.Model):
    name = models.CharField("Name of dynamic table", max_length=30)

    def __str__(self):
        return self.name


class DynamicTableColumn(models.Model):
    SUPPORTED_TYPES = [
        ("BOOLEAN", "boolean"),
        ("INTEGER", "integer"),
        ("STRING", "string")
    ]
    table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE)
    name = models.CharField("Name of dynamic table column", max_length=30)
    type = models.CharField(
        max_length=10,
        choices=SUPPORTED_TYPES,
        default="STRING"
    )

    def __str__(self):
        return self.name
