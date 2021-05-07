from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Categories, Product, ProductImage, ProductAttribute,ProductAttributeValue, ProductMeta,ProductAttributeAssociation, Banner

class UserForm(UserCreationForm):

    class Meta:
        User = get_user_model()
        #  do not refer user model directly first reference

        model = User
        fields = '__all__'
        # fields = ('email','first_name','last_name','groups','is_active','password1','password2',)

        def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['placeholder'] = 'email'
            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
            self.fields['groups'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserUpdateForm(UserChangeForm):
    password=None
    class Meta:
        User = get_user_model()
        model = User
        fields = ('email','first_name','last_name','groups','is_active')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
        self.fields['groups'].widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):

    class Meta:
        User = get_user_model()
        model = User
        fields = ('email','first_name','last_name','password1','password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'

class CustomerProfileChangeForm(UserChangeForm):
    class Meta:
        User=get_user_model()
        model=User
        fields='__all__'

# class ChangeDetailForm(forms.ModelForm):
#
#     class Meta:
#         User = get_user_model()
#         model = User
#         fields = ('first_name','last_name',)
#
#     def __init__(self, *args, **kwargs):
#         super(ChangeDetailForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].widget.attrs['class'] = 'form-control'
#         self.fields['first_name'].widget.attrs['placeholder'] = 'first_name'
#         self.fields['last_name'].widget.attrs['class'] = 'form-control'
#         self.fields['last_name'].widget.attrs['placeholder'] = 'last_name'

class OldPassForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('old_password', 'new_password' , 'confirm_password')

    def __init__(self, *args, **kwargs):
        super(OldPassForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'old_password'


        self.fields['new_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password'].widget.attrs['placeholder'] = 'new_password'


        self.fields['confirm_password'].widget.attrs['class'] = 'form-control'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'new_password'

class UserGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows': '2'}),
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = ['name','description','parent','status']

    def __init__(self,*args, **kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name of category'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['id'] = "exampleFormControlTextarea3"
        self.fields['description'].widget.attrs['rows'] = 2
        self.fields['parent'].widget.attrs['class'] = 'form-control'
        self.fields['parent'].widget.attrs['placeholder'] = 'Parent of a category'
        # self.fields['created_by'].widget.attrs['class'] = 'form-control'
        # self.fields['created_by'].widget.attrs['placeholder'] = ''
        # self.fields['modify_by'].widget.attrs['class'] = 'form-control'
        # self.fields['modify_by'].widget.attrs['placeholder'] = ''

class ProductAttributeForm(ModelForm):
    class Meta:
        model=ProductAttribute
        fields=['name','description_text']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of attribute'}),
            'description_text':forms.Textarea(attrs={'rows':2,'class':'form-control'})
        }

class ProductAttributeEditForm(ModelForm):
    class Meta:
        model=ProductAttribute
        fields=['name','description_text']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of attribute'}),
            'description_text':forms.Textarea(attrs={'rows':2,'class':'form-control'})
        }

class ProductAttributeValueForm(ModelForm):
    #attribute_name = forms.ModelChoiceField(ProductAttribute.objects.all())

    class Meta:
        model=ProductAttributeValue
        fields=['attribute','value']
        labels={
            'attribute':'Select name of attibute',
            'value':'Value of an attribute'
        }
        widgets={
            'value':forms.TextInput(attrs={'class':'form-control','placeholder':'Value of attribute'}),
            'description_text':forms.Textarea(attrs={'rows':2,'class':'form-control'})
        }

class ProductForm(ModelForm):
    class Meta:
        TRUE_FALSE_CHOICES=[
            (True,'True'),
            (False,'False')
        ]

        model=Product
        fields= ('name','sku','short_description','long_description','product_categories',
                 'price','special_price','special_price_from','special_price_to','status','quantity',
                 'is_featured')

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'sku':forms.TextInput(attrs={'class':'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control','rows':2}),
            'long_description': forms.TextInput(attrs={'class': 'form-control','rows':3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=TRUE_FALSE_CHOICES, attrs={'class': 'form-control'}),
            'special_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_price_from':forms.widgets.SelectDateWidget(),
            'special_price_to':forms.widgets.SelectDateWidget(),
            'is_featured':forms.Select(choices=TRUE_FALSE_CHOICES,attrs={'class':'form-control'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control'}),

        }

        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.fields['product_categories'].widget.attrs['class'] = 'select2'
            self.fields['product_categories'].widget.attrs['multiple'] = 'multiple'
            self.fields['product_categories'].widget.attrs['data-dropdown-css-class'] = "se1lect2-blue"
            self.fields['product_categories'].widget.attrs['style'] = 'width: 100%;'
            self.fields['special_price_from'].widget.attrs['class'] = 'datepicker form-control'
            self.fields['special_price_from'].widget.attrs['autocomplete'] = 'off'
            self.fields['special_price_to'].widget.attrs['class'] = 'datepicker form-control'
            self.fields['special_price_to'].widget.attrs['autocomplete'] = 'off'


class ProductImageForm(ModelForm):

    class Meta:
        TRUE_FALSE_CHOICES = [
            (True, 'True'),
            (False, 'False'),

        ]
        model = ProductImage
        fields = '__all__'
        exclude=['created_by','modified_by','created_date','modified_date']
        labels={'status':'Image status'}

        def __init__(self, *args, **kwargs):
            super(ProductImageForm, self).__init__(*args, **kwargs)
            self.fields['image_name'].widget.attrs['class'] = 'form-control'


class ProductMetaForm(ModelForm):
    class Meta:
        model = ProductMeta
        fields='__all__'
        exclude=['product']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':2}),
            'keywords': forms.Textarea(attrs={'class': 'form-control','rows':2}),

        }

class ProductAttributeAssociationForm(ModelForm):

    class Meta:
        model=ProductAttributeAssociation
        exclude=['product_id']

        widgets={
            'product_attribute_id':forms.Select(attrs={'class':'form-control p-id-changes'}),
            'product_attribute_value_id':forms.Select(attrs={'class':'form-control p-value-changes'})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # initially don't reference any attribute
        self.fields['product_attribute_value_id'].queryset = ProductAttributeValue.objects.none()

        if self.add_prefix('product_attribute_id') in self.data:
            try:
                product_attribute_id = int(self.data.get(self.add_prefix('product_attribute_id')))
                self.fields['product_attribute_value_id'].queryset = ProductAttributeValue.objects.filter(attribute=product_attribute_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['product_attribute_value_id'].queryset=self.instance.product_attribute_id.productattributevalue_set.all()


class BannerForm(ModelForm):

    class Meta:
        model=Banner
        fields='__all__'
        exclude=['created_by','modified_by']
        widgets={
            'file_path':forms.TextInput(attrs={'class':'form-control'}),
        }