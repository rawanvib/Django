from django.db import models
#from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30,blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='products') #upload_to='topics/%Y/%m/%d/'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_Cuisines():
        return Cuisine.objects.all()

    @staticmethod
    def get_all_Cuisines_by_category_id(category_id):
        if category_id:
            return Cuisine.objects.filter(category=category_id)
        else:
            return Cuisine.get_all_Cuisines()