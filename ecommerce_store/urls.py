from django.urls import path
from . import views

from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

from .views import PaymentView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing_page_two, name='landing_page_two'),
    path('product_search', views.product_search, name='product_search'),
    path('blog', views.blog, name='blog'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('subscribe_users', views.subscribe_users, name='subscribe_users'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('login-signup', views.signup_login, name='signup_login'),
    path('login', views.login_func, name='login_func'),
    path('logout_func', views.logout_func, name='logout_func'),
    path('product_detail/<int:pk>', views.product_detail, name='product_detail'),
    path('customer_review', views.customer_review, name='customer_review'),
    path('cart', views.cart, name='cart'),
    path('check_coupon', views.check_coupon, name='check_coupon'),
    path('checkout', views.checkout, name='checkout'),


    path('loyalty_register',views.loyalty_register,name='loyalty_register'),
    path('promotion_register',views.promotion_register,name='promotion_register'),
    path('submit_loyalty_info',views.submit_loyalty_info,name='submit_loyalty_info'),
    path('loyalty_discount_page',views.loyalty_discount_page,name='loyalty_discount_page'),
    path('promotion_coupon_page',views.promotion_coupon_page,name='promotion_coupon_page'),
    path('loyalty_benefit_info',views.loyalty_benefit_info,name='loyalty_benefit_info'),

    # activation email
    path('email/confirmation/<str:activation_key>/', views.email_confirm, name='email_activation'  ),

    path('payment', PaymentView.as_view(), name='payment'),

    # forget password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
