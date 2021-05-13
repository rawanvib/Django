from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255, blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    image=models.ImageField(upload_to='product_images')
    body=models.TextField(blank=True, null=True)
    order=models.IntegerField(blank=True, null=True)
    slug=models.SlugField(default='', blank=True)

    def save(self):
        self.slug=slugify(self.title)
        super(Product, self).save()

    def __str__(self):
        return '%s'% self.title
