from django.urls import path
from . import views

app_name='store'

urlpatterns=[
    path('',views.home_page_view,name="index"),
    path('<int:pk>/',views.category_list,name='category_list'),
    path('register/',views.register_view,name="register"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    path("detail-<int:id>/",views.show_detail,name="detail"),
    path("search_dish",views.search_dish,name="search_dish"),
]
