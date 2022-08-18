from django.db import models
from ckeditor.fields import RichTextField

class Landing_page_one_model(models.Model):
    Mobel_First_Name = models.CharField(max_length=256, blank=True, null=True)
    Mobel_Last_Name = models.CharField(max_length=256, blank=True, null=True)
    Mobel_Email_Address = models.CharField(max_length=256, blank=True, null=True)
    Mobel_Date_of_Birth = models.DateField(max_length=256, blank=True, null=True)
    Mobel_City = models.CharField(max_length=256, blank=True, null=True)
    Mobel_State = models.CharField(max_length=256, blank=True, null=True)
    Mobel_Zip_Code = models.CharField(max_length=256, blank=True, null=True)
    Model_checked_or_not = models.CharField(max_length=256, blank=True, null=True)


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Landing page one model'

class Landing_page_one_model_left(models.Model):
    Mobel_left_content = RichTextField(blank=True, null=True)
    Mobel_left_image = models.ImageField(blank=True, null=True, upload_to='landing_page_one/left_image/')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Landing page one model left side'

class app_1_website_logo(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="landing_page_one/logo/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Website Logo (Webapp-1)'

class Get_In_Touch_app1(models.Model):
    class Meta:
        verbose_name_plural = 'GET IN TOUCH App-1'
    Text = models.TextField()

class social_media_app1(models.Model):
    Url = models.CharField(max_length=255)

    def __str__(self):
        return self.Url

    class Meta:
        verbose_name_plural = 'Social Media App-1'

class subscribe_app1(models.Model):
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Subscribers App-1'

