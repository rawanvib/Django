from django.contrib import admin

# Register your models here.
from .models import User,Categories

class CategoriesAdmin(admin.ModelAdmin):
    list_display=('name','description')

admin.site.register(User)
admin.site.register(Categories)
