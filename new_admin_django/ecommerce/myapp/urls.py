from django.contrib.auth.decorators import login_required
from django.urls import path, re_path


from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.login, name = 'login'),
    # path('register/',views.register, name = 'register'),
    path('logout/',views.logoutUser, name = 'logout'),

    # user management
    path('users/', views.UserList, name='UserList'),
    path('users/user_add', views.UserAdd, name='UserAdd'),
    path('users/user_update/<int:id>', views.UserUpdate, name='UserUpdate'),
    path('users/user_delete/<int:id>', views.UserDelete, name='UserDelete'),
    # path('users/user_change', views.UserChange, name='UserChange'),
    # path('users/user_update/<int:id>/user_change_psw', views.UserChangePsw, name='UserChangePsw'),

    # categories
    path('category/', views.category_list, name='category_list'),
    path('category/add/', views.new_category, name='add_category'),
    # path('category/<int:pk>/', views.detail_category, name='detail_category'),
    path('category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:pk>', views.delete_category, name='delete_category'),

    path('product/',views.product_list,name='ProductList'),
    path('product/add/',views.new_product,name='ProductAdd'),
    path('product/edit/<int:pk>/', views.edit_product, name='ProductEdit'),
    path('product/delete/<int:pk>', views.delete_product, name='ProductDelete'),

    path('productAttribute/',views.Product_Attribute,name='ProductAttribute'),
    path('productAttribute/add/',views.Product_Attribute_Add,name='ProductAttributeAdd'),
    path('productAttribute/edit/<int:id>/',views.Product_Attribute_Edit,name='ProductAttributeEdit'),
    path('productAttribute/delete/<int:id>/',views.Product_Attribute_Delete,name='ProductAttributeDelete'),

    path('productAttributeValue/', views.Product_Attribute_Value, name='ProductAttributeValue'),
    path('productAttributeValue/add/', views.Product_Attribute_Value_Add, name='ProductAttributeValueAdd'),
    path('productAttributeValue/edit/<int:id>/', views.Product_Attribute_Value_Edit, name='ProductAttributeValueEdit'),
    path('productAttributeValue/delete/<int:id>/', views.Product_Attribute_Value_Delete, name='ProductAttributeValueDelete'),
]