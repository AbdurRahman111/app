from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page_three, name='landing_page_three'),
    path('subscribes_app3', views.subscribes_app3, name='subscribes_app3'),
]
