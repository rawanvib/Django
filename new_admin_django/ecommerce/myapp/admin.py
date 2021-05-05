from django.contrib import admin

# Register your models here.
from .models import User,Categories,Product,ProductMeta,ProductAttribute
from .models import ProductAttributeValue, ProductAttributeAssociation, ProductImage

class CategoriesAdmin(admin.ModelAdmin):
    list_display=('name','description','parent','created_by')

admin.site.register(User)

admin.site.register(Categories, CategoriesAdmin)


admin.site.register(Product)
admin.site.register(ProductMeta)


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('name',)
admin.site.register(ProductAttribute,ProductAttributeAdmin)

admin.site.register(ProductAttributeValue)
admin.site.register(ProductAttributeAssociation)
admin.site.register(ProductImage)

