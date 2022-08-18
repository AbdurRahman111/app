from django.db import models

from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
# Create your models here.


class EmailConfirmed(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key=models.CharField(max_length=500)
    email_confirmed=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural='User Email-Confirmed'

@receiver(post_save, sender=User)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        dt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_confirmed_instance=EmailConfirmed(user=instance)
        user_encoded=f'{instance.email}-{dt}'.encode()
        activation_key=hashlib.sha224(user_encoded).hexdigest()
        email_confirmed_instance.activation_key=activation_key
        email_confirmed_instance.save()




class Stripe_Api(models.Model):
    class Meta:
        verbose_name_plural = 'STRIPE API'
    Name = models.CharField(max_length=255)
    Publishable_key = models.CharField(max_length=255)
    Secret_key = models.CharField(max_length=255)
    def __str__(self):
        return self.Name


class Get_In_Touch(models.Model):
    class Meta:
        verbose_name_plural = 'GET IN TOUCH'
    Text = models.TextField()




class social_media(models.Model):
    class Meta:
        verbose_name_plural = 'Social Media'
    Url = models.CharField(max_length=255)

    def __str__(self):
        return self.Url




class Home_Banner(models.Model):
    class Meta:
        verbose_name_plural = 'Home Banner'
    Title_one = models.CharField(max_length=255)
    Title_two = models.CharField(max_length=255)
    banner = models.ImageField(upload_to="landing_page_two/Banners/")
    def __str__(self):
        return self.Title_one



class Categories(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    category_name=models.CharField(max_length=500)

    def __str__(self):
        return self.category_name


class products(models.Model):
    class Meta:
        verbose_name_plural = 'Products'
    product_name = models.CharField(max_length=2000)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_price = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='landing_page_two/product_image')
    image2 = models.ImageField(upload_to='landing_page_two/product_image', null=True, blank=True, default='')
    image3 = models.ImageField(upload_to='landing_page_two/product_image', null=True, blank=True, default='')
    image4 = models.ImageField(upload_to='landing_page_two/product_image', null=True, blank=True, default='')
    image5 = models.ImageField(upload_to='landing_page_two/product_image', null=True, blank=True, default='')
    description = models.TextField()

    def __str__(self):
        return self.product_name

    def avarege_review(self):
        filter_product_reviews = reviews.objects.filter(product=self)
        filter_product_reviews_qty = reviews.objects.filter(product=self).count()

        # making average rating
        total_ratings = 0
        for i in filter_product_reviews:
            total_ratings = total_ratings + int(i.ratings)
            # print(total_ratings)
        if filter_product_reviews_qty == 0:
            average_rating = 0
        else:
            average_rating = total_ratings / filter_product_reviews_qty
            print(average_rating)
        average_rating = "%0.1f" % average_rating
        return average_rating

    def product_reviews_qty(self):
        filter_product_reviews_qty = reviews.objects.filter(product=self).count()
        return filter_product_reviews_qty

# class Tracking_the_order(models.Model):
#     order_status_id = models.CharField(max_length=2000)
#     status = models.CharField(max_length=2000)
#
#     def __str__(self):
#         return self.status



class Order(models.Model):
    class Meta:
        verbose_name_plural = 'Orders'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=1000)
    product_details = models.TextField()
    total_bill = models.CharField(max_length=1000)
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    country = models.CharField(max_length=1000)
    street = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    zip = models.CharField(max_length=1000)
    ordered = models.BooleanField(default=False)
    order_date = models.DateField(default=datetime.now, blank=True)
    Your_order_has_been_packed = models.BooleanField(default=False)
    Your_order_is_on_the_way=models.BooleanField(default=False)
    Delivered = models.BooleanField(default=False)


class reviews(models.Model):
    class Meta:
        verbose_name_plural = 'Reviews'
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    ratings = models.CharField(max_length=1)
    review_text = models.TextField()
    review_time = models.DateTimeField(default=datetime.now, blank=True)

class contact_us(models.Model):
    class Meta:
        verbose_name_plural = 'Contact Us'
    email=models.CharField(max_length=200)
    message=models.TextField()

    def __str__(self):
        return self.email


class Contact_Info(models.Model):
    class Meta:
        verbose_name_plural = 'Our Contact Info'
    Address = models.TextField()
    Phone = models.CharField(max_length=255)
    Mail = models.CharField(max_length=255)

    def __str__(self):
        return self.Address + " - " + self.Phone + " - " + self.Mail




class About_Us_Info(models.Model):
    class Meta:
        verbose_name_plural = 'About Us Info'
    Title = models.CharField(max_length=255)
    Details = RichTextField(blank=True, null=True)
    Image = models.ImageField(upload_to="landing_page_two/about_us/")

    def __str__(self):
        return self.Title



class Our_Blog(models.Model):
    class Meta:
        verbose_name_plural = 'Our Blogs'
    Title = models.CharField(max_length=255)
    Details = RichTextField(blank=True, null=True)
    Image = models.ImageField(upload_to="landing_page_two/Blogs/")
    Date = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return self.Title




class subscribe(models.Model):
    class Meta:
        verbose_name_plural = 'Subscribers'
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.email



class app_2_website_logo(models.Model):
    class Meta:
        verbose_name_plural = 'Website Logo (Webapp-2)'
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="landing_page_two/logo/")

    def __str__(self):
        return self.title


class coupon_rate(models.Model):
    class Meta:
        verbose_name_plural = 'Coupon Rate'

    level_name = models.CharField(max_length=255)
    Discount_rate = models.IntegerField()

    def __str__(self):
        return self.level_name


class loyalty_registration_table(models.Model):
    class Meta:
        verbose_name_plural = 'Loyalty Registration Table'

    Customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Full_Name = models.CharField(max_length=255, default='')
    Phone_No = models.CharField(max_length=255, default='')
    Email_id = models.CharField(max_length=255, default='')
    Coupon_rate = models.ForeignKey(coupon_rate, on_delete=models.CASCADE, default='1')
    Discount_percentage = models.IntegerField()
    loyality_Coupon_Code = models.CharField(max_length=255)

    def __str__(self):
        return str(self.Discount_percentage) + "%"



class loyalty_benefit_info_table(models.Model):
    class Meta:
        verbose_name_plural = 'Loyalty Benefit Info Table'

    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title


class any_product_discount(models.Model):
    class Meta:
        verbose_name_plural = 'Any Product Discount'

    title = models.CharField(max_length=255)
    Discount_percentage = models.IntegerField()
    Promotional_deals_Coupon_Code = models.CharField(max_length=255)
    image = models.ImageField(upload_to='landing_page_two/promotional_deals_img')

    def __str__(self):
        return self.title + " - " + str(self.Discount_percentage) + "% - " + self.Promotional_deals_Coupon_Code


class Category_level_discount(models.Model):
    class Meta:
        verbose_name_plural = 'Category Level Discount'

    Category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    Discount_percentage = models.IntegerField()
    Promotional_deals_Coupon_Code = models.CharField(max_length=255)
    image = models.ImageField(upload_to='landing_page_two/promotional_deals_img')

    def __str__(self):
        return str(self.Discount_percentage) + "% - " + self.Promotional_deals_Coupon_Code


class Specific_Level_Product_Deals(models.Model):
    class Meta:
        verbose_name_plural = 'Specific Level Product Discount'

    product = models.ForeignKey(products, on_delete=models.CASCADE)
    Discount_percentage = models.IntegerField()
    Promotional_deals_Coupon_Code = models.CharField(max_length=255)

    def __str__(self):
        return str(self.Discount_percentage) + "% - " + self.Promotional_deals_Coupon_Code

