from django.contrib import admin
from .models import Category, Product
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','category']


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
