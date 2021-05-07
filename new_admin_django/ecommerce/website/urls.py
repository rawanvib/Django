from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),
    path('category_item/<int:id>/', views.category_item, name='category_item'),
    path('product_detail/<int:id>/', views.ProductDetail, name='ProductDetail'),
    path('add_to_wishlist/<int:id>/',views.add_to_wishlist,name='add_to_wishlist'),
]
