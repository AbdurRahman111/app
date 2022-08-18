from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('profile', views.ProfileView.as_view(), name='user-profile'),
    path('edit-profile', views.EditProfileView.as_view(), name='edit-user-profile'),
    path('user-list', views.UserListView.as_view(), name='user-list'),
    path('suspend-user/<str:username>', views.SuspendUserView.as_view(), name='suspend-user'),
    path('activate-user/<str:username>', views.ActivateUserView.as_view(), name='activate-user'),
    path('configure-ad-providers', views.CampaignConfigurationView.as_view(), name='configure-ad-providers'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
]