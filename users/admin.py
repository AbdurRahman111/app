from django.contrib import admin
from .models import Profile, AdsConfigurations, SubscriptionsDetails, Subscriptions, SubscriptionPackages, PackageApps

class ProfileFilters(admin.ModelAdmin):
	list_display = ('id', 'user', 'gender', 'date_of_birth', 'profile_image')
	list_filter = ('gender',)
	# search_fields = ('experiment_name')

class SubscriptionsDetailsFilters(admin.ModelAdmin):
	list_display = ('id', 'user', 'subscription_id', 'subscription_plan', 'company_id')
	list_filter = ('subscription_plan',)

class AdminConfigurationFilters(admin.ModelAdmin):
	list_display = ('service_provider', 'access_key', 'audience_id', 'secret_key', 'app_id', 'developer_token', 'client_id', 'refresh_token')
	list_filter = ('service_provider',)
	search_fields = ('service_provider',)


class SubscriptionsFilters(admin.ModelAdmin):
	list_display = ('id', 'subscription_id', 'subscription_plan', 'subscription_type', 'subscription_name')
	list_filter = ('subscription_type',)
	search_fields = ('subscription_name',)

class SubscriptionPackagesFilters(admin.ModelAdmin):
	list_display = ('id', 'name')
	search_fields = ('name',)

class PackageAppsFilters(admin.ModelAdmin):
	list_display = ('id', 'app_name', 'package')
	search_fields = ('app_name',)

admin.site.register(Subscriptions, SubscriptionsFilters)

admin.site.register(Profile, ProfileFilters)
admin.site.register(SubscriptionsDetails, SubscriptionsDetailsFilters)
admin.site.register(AdsConfigurations, AdminConfigurationFilters)
admin.site.register(SubscriptionPackages, SubscriptionPackagesFilters)
admin.site.register(PackageApps, PackageAppsFilters)
