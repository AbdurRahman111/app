from django.db import models

# Create your models here.



class website_logo(models.Model):
    class Meta:
        verbose_name_plural = 'Website Logo (Webapp-3)'
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="landing_page_two/logo/")

    def __str__(self):
        return self.title



class any_product_discount(models.Model):
    class Meta:
        verbose_name_plural = 'Any Product Discount'
    title = models.CharField(max_length=255)
    Discount_percentage = models.IntegerField()
    Promotional_deals_Coupon_Code = models.CharField(max_length=255)
    image = models.ImageField(upload_to='promotional_deals_img')

    def __str__(self):
        return self.title + " - " + str(self.Discount_percentage) + "% - " + self.Promotional_deals_Coupon_Code


class Category_level_discount(models.Model):
    class Meta:
        verbose_name_plural = 'Category Level Discount'
    Category = models.CharField(max_length=255)
    Discount_percentage = models.IntegerField()
    Promotional_deals_Coupon_Code = models.CharField(max_length=255)
    image = models.ImageField(upload_to='promotional_deals_img')

    def __str__(self):
        return str(self.Discount_percentage) + "% - " + self.Promotional_deals_Coupon_Code


class Specific_Level_Product_Deals(models.Model):
    class Meta:
        verbose_name_plural = 'Specific Level Product Discount'
    product = models.CharField(max_length=255)
    Discount_percentage = models.IntegerField()
    Promotional_deals_Coupon_Code = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Specific_promotional_deals_img', blank=True, null=True)

    def __str__(self):
        return str(self.Discount_percentage)+"% - "+ self.Promotional_deals_Coupon_Code



class Get_In_Touch_app_3(models.Model):
    class Meta:
        verbose_name_plural = 'GET IN TOUCH App-3'
    Text = models.TextField()




class social_media_app_3(models.Model):
    class Meta:
        verbose_name_plural = 'Social Media App-3'
    Url = models.CharField(max_length=255)

    def __str__(self):
        return self.Url




class subscribe_app_3(models.Model):
    class Meta:
        verbose_name_plural = 'Subscribers App-3'
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.email

