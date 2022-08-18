from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing_page_five, name='landing_page_five'),
    path('Register_info_for_five/', views.Register_info_for_five, name='Register_info_for_five'),
    path('subscribes_app5/', views.subscribes_app5, name='subscribes_app5'),


]
