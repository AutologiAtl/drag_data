from django.db import models

# Create your models here.
# models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class YourModel(models.Model):
    field1 = models.CharField(max_length=100,null=True, blank=True)
    field2 = models.CharField(max_length=100,null=True, blank=True)
    field3 = models.CharField(max_length=100,null=True, blank=True)
    field4 = models.CharField(max_length=100,null=True, blank=True)
    field5 = models.CharField(max_length=100,null=True, blank=True)
    field6 = models.CharField(max_length=100,null=True, blank=True)
    field7 = models.CharField(max_length=100,null=True, blank=True)
    field8 = models.CharField(max_length=100,null=True, blank=True)
    field9 = models.CharField(max_length=100,null=True, blank=True)
    field10 = models.CharField(max_length=100,null=True, blank=True)
    field11 = models.CharField(max_length=100,null=True, blank=True)
    field12 = models.CharField(max_length=100,null=True, blank=True)
    field13 = models.CharField(max_length=100,null=True, blank=True)
    field14 = models.CharField(max_length=100,null=True, blank=True)
    # Add more fields as needed

