from django.db import models



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='products')

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
