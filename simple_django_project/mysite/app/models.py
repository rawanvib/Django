from django.db import models

# Create your models here.
class Pizza(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField()
    price=models.IntegerField()
    image=models.ImageField(upload_to='pics')

class Salad(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField()
    price=models.IntegerField()
    image=models.ImageField(upload_to='pics')

class Noodle(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField()
    price=models.IntegerField()
    image=models.ImageField(upload_to='pics')
