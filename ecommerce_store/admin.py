from django.contrib import admin
from .models import EmailConfirmed, Categories, products, Order, contact_us, reviews, subscribe, app_2_website_logo, loyalty_registration_table, loyalty_benefit_info_table, coupon_rate, any_product_discount, Category_level_discount, Specific_Level_Product_Deals, Contact_Info, About_Us_Info, Our_Blog, Home_Banner, Stripe_Api, Get_In_Touch, social_media

# Register your models here.

class EmailConfirmedAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'activation_key', 'email_confirmed']

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

admin.site.register(EmailConfirmed, EmailConfirmedAdmin)
admin.site.register(Categories)
admin.site.register(products)
admin.site.register(Order)
admin.site.register(contact_us)
admin.site.register(reviews)
admin.site.register(subscribe)
admin.site.register(app_2_website_logo)
admin.site.register(Contact_Info)
admin.site.register(About_Us_Info)
admin.site.register(Our_Blog)
admin.site.register(Home_Banner)
admin.site.register(Stripe_Api)
admin.site.register(Get_In_Touch)
admin.site.register(social_media)




class show_loyalty_registration_table(admin.ModelAdmin):
    list_display = ['Customer', 'Full_Name', 'Discount_percentage', 'loyality_Coupon_Code']
admin.site.register(loyalty_registration_table, show_loyalty_registration_table)

admin.site.register(loyalty_benefit_info_table)
admin.site.register(coupon_rate)


class show_any_product_discount(admin.ModelAdmin):
    list_display = ['title', 'Discount_percentage', 'Promotional_deals_Coupon_Code']
admin.site.register(any_product_discount,show_any_product_discount)


class show_Category_level_discount(admin.ModelAdmin):
    list_display = ['Category', 'Discount_percentage', 'Promotional_deals_Coupon_Code']
admin.site.register(Category_level_discount,show_Category_level_discount)


class show_Specific_Level_Product_Deals(admin.ModelAdmin):
    list_display = ['product', 'Discount_percentage', 'Promotional_deals_Coupon_Code']
admin.site.register(Specific_Level_Product_Deals,show_Specific_Level_Product_Deals)
