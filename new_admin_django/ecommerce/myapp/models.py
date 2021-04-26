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


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name