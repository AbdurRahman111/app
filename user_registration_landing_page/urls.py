from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page_one, name='landing_page_one'),
    path('Register_info/', views.Register_info, name='Register_info'),
    path('check_Email_Address_is_exist/', views.check_Email_Address_is_exist, name='check_Email_Address_is_exist'),
    path('subscribes_app2/', views.subscribes_app2, name='subscribes_app2'),
]
