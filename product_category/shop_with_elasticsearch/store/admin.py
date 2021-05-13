from django.contrib import admin
from .models import Category, Cuisine
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']

class CuisineAdmin(admin.ModelAdmin):
    list_display=['title','price','category']


admin.site.register(Cuisine,CuisineAdmin)
admin.site.register(Category,CategoryAdmin)
