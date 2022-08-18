from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Landing_page_four_model(models.Model):
    class Meta:
        verbose_name_plural = 'Landing page Four model'

    Mobel_Name = models.CharField(max_length=256, blank=True, null=True)
    Mobel_Email_Address = models.CharField(max_length=256, blank=True, null=True)
    Mobel_Address = models.CharField(max_length=256, blank=True, null=True)
    Mobel_donate_amount = models.CharField(max_length=256, blank=True, null=True)
    Model_checked_or_not = models.CharField(max_length=256, blank=True, null=True)


    def __str__(self):
        return str(self.id)

class Landing_page_four_model_left(models.Model):
    class Meta:
        verbose_name_plural = 'Landing page four model left side'


    Mobel_left_content = RichTextField(blank=True, null=True)
    Mobel_left_image = models.ImageField(blank=True, null=True, upload_to='landing_page_four/left_image/')

    def __str__(self):
        return str(self.id)


class app_4_website_logo(models.Model):
    class Meta:
        verbose_name_plural = 'Website Logo (Webapp-4)'
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="landing_page_four/logo/")

    def __str__(self):
        return self.title




class Get_In_Touch_app_4(models.Model):
    class Meta:
        verbose_name_plural = 'GET IN TOUCH App-4'
    Text = models.TextField()




class social_media_app_4(models.Model):
    class Meta:
        verbose_name_plural = 'Social Media App-4'
    Url = models.CharField(max_length=255)

    def __str__(self):
        return self.Url




class subscribe_app_4(models.Model):
    class Meta:
        verbose_name_plural = 'Subscribers App-4'
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.email

