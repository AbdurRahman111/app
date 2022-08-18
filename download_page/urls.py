from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing_page_seven, name='landing_page_seven'),
    # path('Register_info_for_seven/', views.Register_info_for_seven, name='Register_info_for_seven'),
    path('download/', views.download_file, name='download_file'),
    path('download_file_from_link/', views.download_file_from_link, name='download_file_from_link'),
    path('clear_seassion/', views.clear_seassion, name='clear_seassion'),
    path('subscribes_app7/', views.subscribes_app7, name='subscribes_app7'),


]
