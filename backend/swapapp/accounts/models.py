from django.db import models

class Swap(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=50)
    description = models.TextField(max)
    is_active = models.BooleanField()
    is_home = models.BooleanField()
    
    class Category(models.Model):
        name = models.CharField(max_length=150)
