from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt

Gender_Option = (
	('Male', 'Male'),
	('Female', 'Female'),
	('Do not want to respond', 'Do not want to respond')
)

App_Options = (
	('Surveyscaled', 'Surveyscaled'),
	('Testscaled', 'Testscaled'),
	('User Registration Landing Page', 'User Registration Landing Page'),
	('Download Landing Page', 'Download Landing Page'),
	('E-commerce Site Management', 'E-commerce Site Management'),
	('Price Pormotion Landing Page', 'Price Pormotion Landing Page'),
	('Video Landing Page', 'Video Landing Page'),
	('Donation Landing Page', 'Donation Landing Page'),
	('Event Registration Landing Page', 'Event Registration Landing Page')
)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
	gender = models.CharField(max_length=21, null=True, blank=True, verbose_name='Gender')
	date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date of Birth')
	profile_image = models.FileField(upload_to='users/profile', default='profile_logo.jpg', blank=True, null=True, verbose_name='Profile Image')

	def __str__(self):
		return f'User: {self.user}, Profile #: {self.pk}'

	class Meta:
		verbose_name_plural = 'Profiles'

class SubscriptionsDetails(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_subscription')
	subscription_id = models.CharField(max_length=250, verbose_name='Subscription Id')
	company_id = models.CharField(max_length=250, verbose_name='Company Id')
	subscription_plan = models.CharField(max_length=150, verbose_name='Subscription Plan')

	def __str__(self):
		return f'User: {self.user}, Subscription instance: {self.id}'

	def get_package(self):
		package = SubscriptionPackages.objects.get(name=self.subscription_plan)
		apps = PackageApps.objects.filter(package=package)
		return apps

	class Meta:
		verbose_name_plural = 'Subscription Details'

class AdsConfigurations(models.Model):
	service_provider = models.CharField(max_length=100, verbose_name='Service Provider')
	access_key = encrypt(models.CharField(max_length=150, null=True, blank=True, verbose_name='Access Key'))
	secret_key = encrypt(models.CharField(max_length=150, null=True, blank=True, verbose_name='Secret Key'))
	audience_id = encrypt(models.CharField(max_length=150, null=True, blank=True, verbose_name='Audience Id'))
	app_id = encrypt(models.CharField(max_length=150, null=True, blank=True, verbose_name='App Id'))
	developer_token = encrypt(models.CharField(max_length=150, null=True, blank=True, verbose_name='Developer Token'))
	client_id = encrypt(models.CharField(max_length=150, null=True, blank=True, verbose_name='Client Id'))
	client_secret = encrypt(models.CharField(max_length=150, null=True, blank=True, verbose_name='Client Secret'))
	refresh_token = encrypt(models.CharField(max_length=150, null=True, blank=True, verbose_name='Refresh Token'))

	def __str__(self):
		return f'{self.pk} Provider {self.service_provider}'

	class Meta:
		verbose_name_plural = 'Ads Configuration'

class SubscriptionPackages(models.Model):
	name = models.CharField(max_length=150, unique=True)

	def get_apps_list(self):
		package = PackageApps.objects.filter(package=self)
		return package

	def __str__(self):
		return self.name

class PackageApps(models.Model):
	app_name = models.CharField(max_length=150, choices=App_Options)
	package = models.ForeignKey('SubscriptionPackages', on_delete=models.CASCADE)

	def __str__(self):
		return self.app_name



# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class User(models.Model):
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    email = models.CharField(unique=True, max_length=150, blank=True, null=True)
    password = models.BinaryField(blank=True, null=True)
    authenticated = models.BooleanField(blank=True, null=True)
    email_confirmation_sent_on = models.DateTimeField(blank=True, null=True)
    email_confirmed = models.BooleanField(blank=True, null=True)
    email_confirmed_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'

class Company(models.Model):
    company_id = models.CharField(unique=True, max_length=150)
    company_name = models.CharField(unique=True, max_length=150)
    group = models.CharField(max_length=150)
    company_address = models.CharField(max_length=250)
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    company_phone = models.CharField(max_length=150)
    company_email = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=150)
    contact_email = models.CharField(max_length=150)
    contact_phone = models.CharField(max_length=150)
    date = models.DateField()
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'company'

class SubscriptionDetails(models.Model):
    subscription_id = models.CharField(max_length=25, blank=True, null=True)
    stripeid = models.CharField(max_length=150, blank=True, null=True)
    payment = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription_details'


class Subscriptions(models.Model):
    subscription_id = models.CharField(max_length=25, blank=True, null=True)
    subscription_plan = models.CharField(max_length=150)
    subscription_type = models.CharField(max_length=150)
    subscription_name = models.CharField(max_length=150)
    product_group_count = models.IntegerField()
    ncountry = models.IntegerField()
    store_category_count = models.IntegerField()
    n_users = models.IntegerField()
    n_data_loads = models.IntegerField()
    status = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    setup_price = models.FloatField()
    base_monthly_unit_price = models.FloatField()
    base_monthly_unit_discount = models.FloatField()
    contracted_installments = models.IntegerField()
    max_number_of_markets = models.IntegerField()
    max_installments = models.IntegerField()
    total_monthly_amount = models.FloatField()
    create_date = models.DateField()
    company = models.ForeignKey('Company', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'subscriptions'