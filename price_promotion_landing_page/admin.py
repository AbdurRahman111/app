from django.contrib import admin
from .models import any_product_discount, Category_level_discount, Specific_Level_Product_Deals, website_logo, Get_In_Touch_app_3, social_media_app_3,subscribe_app_3
# Register your models here.


class show_any_product_discount(admin.ModelAdmin):
    list_display = ['title', 'Discount_percentage', 'Promotional_deals_Coupon_Code']
admin.site.register(any_product_discount,show_any_product_discount)


class show_Category_level_discount(admin.ModelAdmin):
    list_display = ['Category', 'Discount_percentage', 'Promotional_deals_Coupon_Code']
admin.site.register(Category_level_discount,show_Category_level_discount)


class show_Specific_Level_Product_Deals(admin.ModelAdmin):
    list_display = ['product', 'Discount_percentage', 'Promotional_deals_Coupon_Code']
admin.site.register(Specific_Level_Product_Deals,show_Specific_Level_Product_Deals)


admin.site.register(website_logo)
admin.site.register(Get_In_Touch_app_3)
admin.site.register(social_media_app_3)
admin.site.register(subscribe_app_3)