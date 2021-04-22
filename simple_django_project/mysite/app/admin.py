from django.contrib import admin
from .models import Pizza,Salad,Noodle
# Register your models here.
admin.site.register((Pizza,Salad,Noodle))
