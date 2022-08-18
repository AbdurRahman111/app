
from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing_page_four, name='landing_page_four'),
    path('Register_info_four/', views.Register_info_four, name='Register_info_four'),
    path('landing_page_four_second_page', views.landing_page_four_second_page, name='landing_page_four_second_page'),
    path('subscribes_app4', views.subscribes_app4, name='subscribes_app4'),
]
