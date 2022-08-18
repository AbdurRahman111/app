from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing_page_eight, name='landing_page_eight'),
    path('Register_info_for_eight/', views.Register_info_for_eight, name='Register_info_for_eight'),
    path('subscribes_app8/', views.subscribes_app8, name='subscribes_app8'),
    # path('landing_page_four_second_page', views.landing_page_four_second_page, name='landing_page_four_second_page'),
]
