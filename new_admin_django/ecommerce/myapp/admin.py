from django.contrib import admin

# Register your models here.
from .models import User,Categories

admin.site.register(User)
admin.site.register(Categories)
