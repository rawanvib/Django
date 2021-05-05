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


	def get_full_name(self):
		"""
		returns the first_name plus the last name, with a space inbetween
		"""
		full_name='%s %s' % (self.first_name, self.last_name)
		return full_name.strip()



#------------------------category----------------------------------#
class Categories(models.Model):
	name=models.CharField(max_length=150)
	description=models.TextField()
	parent=models.CharField(max_length=150)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,related_name='catagory_created_by',default='',null=True,blank=True)
	created_date=models.DateField(auto_now_add=True)
	modify_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
								  related_name='catogory_modify_by', default='', null=True, blank=True)
	modified_date = models.DateField(auto_now=True)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	class meta:
		ordering = ['-created_date']
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

#----------------------product--------------------#

class Product(models.Model):
	name = models.CharField(max_length=100)
	sku = models.CharField(max_length=45)
	short_description = models.CharField(max_length=100)
	long_description = models.TextField(max_length=250)
	product_categories = models.ManyToManyField(Categories)
	price = models.DecimalField(max_digits=14, decimal_places=2)
	special_price = models.DecimalField(max_digits=14, decimal_places=2)
	special_price_from = models.DateField(blank=True, null=True)
	special_price_to = models.DateField(blank=True, null=True)
	status = models.BooleanField(default=False)
	quantity = models.IntegerField(null=True,validators=[MinValueValidator(0)])
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
								   related_name='product_created_by', default='', null=True, blank=True)
	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
								  related_name='product_modified_by', default='', null=True, blank=True)
	is_featured=models.BooleanField(default=False)


	def __str__(self):
		return self.name

	@property
	def is_new(self):
		time_between_insertion = date.today() - self.created_date

		if time_between_insertion.days > 15:
			return False
		else:
			return True

	@property
	def special_price_test(self):
		if self.special_price and self.special_price_from and self.special_price_to:
			if date.today() > self.special_price_from and date.today() < self.special_price_to:
				return True
			else:
				return False
		else:
			return False

class ProductMeta(models.Model):
	product = models.OneToOneField(Product, on_delete=models.DO_NOTHING)
	title = models.CharField(max_length=45)
	keywords=models.TextField()
	description = models.TextField(max_length=250)

# class ProductCategory(models.Model):
# 	category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
# 	product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

class ProductAttribute(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description_text = models.TextField(null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
								   related_name='product_attribute_created_by', default='', null=True, blank=True)
	modified_date = models.DateTimeField(auto_now=True)
	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_attribute_modified_by', default='', null=True, blank=True)
# products = models.ManyToManyField('Product', related_name="attributes")

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'product_atttribute'
		verbose_name = 'product attribute'
		verbose_name_plural = 'product attributes'

class ProductAttributeValue(models.Model):
	attribute = models.ForeignKey(ProductAttribute, on_delete=models.DO_NOTHING)
	value = models.CharField(max_length=45)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_attribute_value_created_by',default='', null=True, blank=True)
	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_attribute_value_modified_by',default='', null=True, blank=True)

	def __str__(self):
		return self.value


class ProductImage(models.Model):
	# def upload_path(self, filename):
	# 	return 'static/uploads/image_%s%s' % (timezone.now().strftime('%Y/%m/%d/%Y%m%d_'), filename)

	product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
	status = models.BooleanField(default=False)
	image_name = models.ImageField(upload_to='products/product_images')
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_image_created_by',default='', null=True, blank=True)
	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='product_image_modify_by',default='', null=True, blank=True)

	def __unicode__(self):
		return self.name


class ProductAttributeAssociation(models.Model):
	product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
	product_attribute_id = models.ForeignKey(ProductAttribute, on_delete=models.DO_NOTHING)
	product_attribute_value_id = models.ForeignKey(ProductAttributeValue, on_delete=models.DO_NOTHING)


#____________________________________banner____________________________#
class Banner(models.Model):
	STATUS_CHOICE=(
		('Active', 'Active'),
		('Inactive', 'Inactive'),
	)
	status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='Inactive')
	file_path = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
								   related_name='banner_uploaded_by', default='', null=True, blank=True)
	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
									related_name='banner_modified_by', default='', null=True, blank=True)
