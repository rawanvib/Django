from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='app'

urlpatterns = [
    path('',views.home_page_view,name="index"),
    path('app/register/',views.register_view,name="register"),
    path("app/login/",views.login,name="login"),
    path("app/logout/",views.logout,name="logout"),
    path("app/<int:image_id>/",views.show_detail,name="show_detail"),
    path("app/<int:pk>/",views.show_detail_salad,name="show_detail_salad")
]
# to grab the integer of the id
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
