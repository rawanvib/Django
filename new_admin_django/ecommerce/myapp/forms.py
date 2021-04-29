from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Categories

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

    class Meta:
        User = get_user_model()
        model = User
        fields = ('email','first_name','last_name','groups','is_active')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['id'] = 'exampleInputEmail1'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
        self.fields['groups'].widget.attrs['class'] = 'form-control'


# class RegisterForm(UserCreationForm):
#
#     class Meta:
#         User = get_user_model()
#         model = User
#         fields = ('email','first_name','last_name','password1','password2',)
#
#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)
#         self.fields['email'].widget.attrs['class'] = 'form-control'
#         self.fields['email'].widget.attrs['placeholder'] = 'email'
#         self.fields['first_name'].widget.attrs['class'] = 'form-control'
#         self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
#         self.fields['last_name'].widget.attrs['class'] = 'form-control'
#         self.fields['last_name'].widget.attrs['placeholder'] = 'last name'
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].widget.attrs['placeholder'] = 'password'
#         self.fields['password2'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'


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



class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(CategoryForm,self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name of category'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['id'] = "exampleFormControlTextarea3"
        self.fields['description'].widget.attrs['rows'] = 2
        self.fields['parent'].widget.attrs['class'] = 'form-control'
        self.fields['parent'].widget.attrs['placeholder'] = 'Parent of a category'
        self.fields['created_by'].widget.attrs['class'] = 'form-control'
        self.fields['created_by'].widget.attrs['placeholder'] = ''
        self.fields['modified_by'].widget.attrs['class'] = 'form-control'
        self.fields['modified_by'].widget.attrs['placeholder'] = ''
        self.fields['created_date'].widget.attrs['class'] = 'form-control'
        self.fields['created_date'].widget.attrs['value'] = 'YYYY-MM-DD'
        self.fields['modified_date'].widget.attrs['class'] = 'form-control'
        self.fields['modified_date'].widget.attrs['value'] = 'YYYY-MM-DD'


