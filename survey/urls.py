from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('surveyscaled/', include('surveyscaled.urls')),
    path('media-scaled/', include('experiment.urls')),
    path('users/', include('users.urls')),
    path('lp_usrreg/', include('user_registration_landing_page.urls')),
    path('lp_ecomm/', include('ecommerce_store.urls')),
    path('lp_promo/', include('price_promotion_landing_page.urls')),
    path('lp_charity/', include('charity_donation_app.urls')),
    path('lp_event/', include('event_registration_page.urls')),
    path('lp_download/', include('download_page.urls')),
    path('lp_video/', include('video_view_page.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
