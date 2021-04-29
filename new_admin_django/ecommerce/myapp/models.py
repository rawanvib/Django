from datetime import date, datetime

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True,null=False,blank=False)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('staff status'),default=False)
	#is_admin	= models.BooleanField(default=False)



	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []



#----------------------product--------------------#
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sku = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=150, default="")
    modified_by = models.CharField(max_length=200, default="")



    def __str__(self):
        return self.name

class ProductMeta(models.Model):
    product = models.OneToOneField('Product', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

class ProductImage(models.Model):
    def upload_path(self, filename):
        return 'static/uploads/images/%s%s' % (timezone.now().strftime('%Y/%m/%d/%Y%m%d_'), filename)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    default = models.BooleanField()
    image = models.ImageField(upload_to='products')

    def __unicode__(self):
        return self.name

class ProductCharacteristic(models.Model):
    product = models.ForeignKey('Product', related_name="characteristics", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class ProductAttribute(models.Model):
    category = models.ForeignKey('Categories', on_delete=models.DO_NOTHING)
    products = models.ManyToManyField('Product', related_name="attributes")
    name = models.CharField(max_length=100)
    ordering = ['-category']
    def __unicode__(self):
        return u'%s : %s' % (self.category, self.name)

# class ProductAttributeCategory(models.Model):
#     name = models.CharField(max_length=100)
#     def __unicode__(self):
#         return self.name

class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey('ProductAttribute', related_name="values", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name



#------------------------category----------------------------------#
class Categories(models.Model):
	name=models.CharField(max_length=150)
	description=models.TextField()
	parent=models.CharField(max_length=150)
	created_by=models.CharField(max_length=150, default="admin")
	created_date=models.DateField()
	modified_by=models.CharField(max_length=200,default="admin")
	modified_date=models.DateField()
	status=models.BooleanField(default=False)
