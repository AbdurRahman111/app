from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from django.core.validators import FileExtensionValidator


class Landing_page_seven_model(models.Model):
    class Meta:
        verbose_name_plural = 'Landing page seven model'

    Model_First_Name = models.CharField(max_length=256, blank=True, null=True)
    Model_Last_Name = models.CharField(max_length=256, blank=True, null=True)
    Model_Email_Address = models.CharField(max_length=256, blank=True, null=True)
    Model_country_Address = models.CharField(max_length=256, blank=True, null=True)
    Model_checked_or_not = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Landing_page_seven_model_left(models.Model):
    class Meta:
        verbose_name_plural = 'Landing page seven model left side'

    Model_full_image = models.ImageField(blank=True, null=True, upload_to='landing_page_seven/full_image/')
    Model_left_content_top = RichTextField(blank=True, null=True)
    Model_content_image = models.ImageField(blank=True, null=True, upload_to='landing_page_seven/content_image/')
    Model_left_content_bottom = RichTextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class app_7_website_logo(models.Model):
    class Meta:
        verbose_name_plural = 'Website Logo (Webapp-7)'
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="landing_page_seven/logo/")

    def __str__(self):
        return self.title


class Get_In_Touch_app_7(models.Model):
    class Meta:
        verbose_name_plural = 'GET IN TOUCH App-7'
    Text = models.TextField()




class social_media_app_7(models.Model):
    class Meta:
        verbose_name_plural = 'Social Media App-7'
    Url = models.CharField(max_length=255)

    def __str__(self):
        return self.Url




class subscribe_app_7(models.Model):
    class Meta:
        verbose_name_plural = 'Subscribers App-7'
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.email
