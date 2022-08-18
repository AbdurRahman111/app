from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
	CreateView,
	View,
	ListView,
)
from django.contrib.auth.views import LoginView
from users.forms import (
	SignUpForm,
	UserUpdateForm,
	ProfileUpdateForm,
)
from .models import (
	SubscriptionsDetails,
	AdsConfigurations,
	Company,
	Subscriptions,
)
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import login

# Sign Up View
class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('core:home')
    success_message = "User registered successfuly"
    template_name = 'signup.html'

class LoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_field_name = 'core:home'

class RegistrationView(View):
	template_name = 'authentication/registration_page.html'

	def get(self, request):
		context = {
			'title'		:	'Crunchscaled - Registration Page',
		}
		return render(request, self.template_name, context)

	def post(self, request):
		# Fetching user account details
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		# Fetching subscription details
		company_id = request.POST.get('company_id')
		subscription_id = request.POST.get('subscription_id')

		# Validating if company is registered in database of flask application
		try:
			company_obj = Company.objects.using('testdatabase').get(company_id=company_id)

		except Company.DoesNotExist:
			context = {
				'title'		:	'Crunchscaled - Registration Page',
			}
			messages.error(request, "Your company id is not correct. Please provide valid company id")
			return render(request, self.template_name, context)

		# Validating if subscription id is registered in database of flask application
		try:
			subscription_obj = Subscriptions.objects.using('testdatabase').get(subscription_id=subscription_id, subscription_type='CRUNCH')

		except Subscriptions.DoesNotExist:
			context = {
				'title'		:	'Crunchscaled - Registration Page',
			}
			messages.error(request, "Your subscription id is not correct. Please provide valid subscription id")
			return render(request, self.template_name, context)


		try:
			users = User.objects.get(username=username)
			context = {
				'title'		:	'Crunchscaled - Registration Page',
			}
			messages.error(request, "Username already registered! Please use a different username")
			return render(request, self.template_name, context)

		except User.DoesNotExist:
			pass

		# Checking if both passwords are same
		if password1 == password2:
			# Creating user accoumt
			user_obj = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)

		else:
			context = {
				'title'		:	'Crunchscaled - Registration Page',
			}
			messages.error(request, "Passwords doesn't match. Please make sure that both passwords are same")
			return render(request, self.template_name, context)

		try:
			# Saving subscription details
			subscription_obj = SubscriptionsDetails(user=user_obj,
				subscription_id = subscription_id,
				company_id = company_id,
				subscription_plan = subscription_obj.subscription_plan
			)
			subscription_obj.save()

		except Exception as exc:
			print('Error: ',exc)
			user_obj.delete()
			context = {
				'title'		:	'Crunchscaled - Registration Page',
			}
			messages.error(request, "Please make sure that all the information in step 2 is provided")
			return render(request, self.template_name, context)

		login(request, user_obj)
		messages.success(request, "Registration successful." )
		return redirect('core:home')

class ProfileView(View):
	template_name = 'profile.html'

	def get(self, request):
		if request.user.first_name:
			title = request.user.first_name
		else:
			title = request.user.username

		current_user = request.user

		context = {
			'title'	: 'Profile Dashboard',
			'user'	: current_user,
			}
		return render(request, self.template_name, context)

class EditProfileView(View):
	template_name = 'edit_profile.html'

	def get(self, request):
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.user_profile)

		context = {
			'title': 'Update Profile Information',
			'u_form': u_form,
			'p_form': p_form,
		}

		return render(request, self.template_name, context)

	def post(self, request):
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been updated successfully.')
			return redirect('users:user-profile')

		else:
			context = {
				'title': 'Update Profile Information',
				'u_form': u_form,
				'p_form': p_form,
			}
			return render(request, self.template_name, context)

class UserListView(ListView):
	template_name = 'user_list.html'
	model = User
	paginate_by = 15
	context_object_name = 'users'
	ordering = ['id']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = "User List"
		return context

class SuspendUserView(View):

	def get(self, request, username):
		try:
			user = User.objects.get(username=username)
			user.is_active = False
			user.save()
			messages.success(request, 'User account suspended.')

		except Exception as exc:
			messages.error(request, "Can't suspend user account!")

		return redirect('users:user-list')

class ActivateUserView(View):

	def get(self, request, username):
		try:
			user = User.objects.get(username=username)
			user.is_active = True
			user.save()
			messages.success(request, 'User account activated.')

		except Exception as exc:
			messages.error(request, "Can't activate user account!")

		return redirect('users:user-list')

class CampaignConfigurationView(View):
	template_name = 'configure_providers.html'

	def get(self, request):
		context = {
			'title'	:	'Testscaled - Setup Campaign Providers',
		}
		return render(request, self.template_name, context)

	def post(self, request):
		# The method will fetch campagin provider from frontend 
		# and will save api data for only the campaign provider selected by user
		campaign_provider = request.POST.get('campaign-provider', None)

		mail_access_key = request.POST.get('mail-api-key', None)
		mail_secret_key = request.POST.get('mail-data-center', None)
		mail_audience_id = request.POST.get('mail-audience-id', None)

		facebook_access_key = request.POST.get('facebook-access-key', None)
		facebook_secret_key = request.POST.get('facebook-secret-key', None)
		facebook_app_id = request.POST.get('facebook-app-id', None)

		google_developer_token = request.POST.get('google-developer-token', None)
		google_client_id = request.POST.get('google-client-id', None)
		google_client_secret = request.POST.get('google-client-secret', None)
		google_refresh_token = request.POST.get('google-refresh-token', None)
		
		if campaign_provider == 'MailChimp':
			try:
				conf_obj = AdsConfigurations.objects.get(service_provider=campaign_provider)
				conf_obj.secret_key = mail_secret_key
				conf_obj.access_key = mail_access_key
				conf_obj.audience_id = mail_audience_id
				conf_obj.save()
			except Exception as exc:
				ads_config_obj = AdsConfigurations(service_provider=campaign_provider, 
					access_key=mail_access_key, 
					secret_key=mail_secret_key, 
					audience_id=mail_audience_id
				)
				ads_config_obj.save()

		elif campaign_provider == 'Facebook':
			try:
				conf_obj = AdsConfigurations.objects.get(service_provider=campaign_provider)
				conf_obj.secret_key = facebook_secret_key
				conf_obj.access_key = facebook_access_key
				conf_obj.app_id = facebook_app_id
				conf_obj.save()

			except Exception as exc:
				ads_config_obj = AdsConfigurations(service_provider=campaign_provider, 
					access_key=facebook_access_key, 
					secret_key=facebook_secret_key, 
					app_id=facebook_app_id
				)
				ads_config_obj.save()

		elif campaign_provider == 'Google':
			try:
				conf_obj = AdsConfigurations.objects.get(service_provider=campaign_provider)
				conf_obj.developer_token = google_developer_token
				conf_obj.client_id = google_client_id
				conf_obj.client_secret = google_client_secret
				conf_obj.refresh_token = google_refresh_token
				conf_obj.save()

			except Exception as exc:
				ads_config_obj = AdsConfigurations(service_provider=campaign_provider, 
					developer_token=google_developer_token, 
					client_id=google_client_id, 
					client_secret=google_client_secret, 
					refresh_token=google_refresh_token
				)
				ads_config_obj.save()

		elif campaign_provider == 'All':
			try:
				conf_obj = AdsConfigurations.objects.get(service_provider='MailChimp')
				conf_obj.secret_key = mail_secret_key
				conf_obj.access_key = mail_access_key
				conf_obj.audience_id = mail_audience_id
				conf_obj.save()
			except Exception as exc:
				ads_config_obj = AdsConfigurations(service_provider='MailChimp', 
					access_key=mail_access_key, 
					secret_key=mail_secret_key, 
					audience_id=mail_audience_id
				)
				ads_config_obj.save()

			try:
				conf_obj = AdsConfigurations.objects.get(service_provider='Facebook')
				conf_obj.secret_key = facebook_secret_key
				conf_obj.access_key = facebook_access_key
				conf_obj.app_id = facebook_app_id
				conf_obj.save()

			except Exception as exc:
				ads_config_obj = AdsConfigurations(service_provider='Facebook', 
					access_key=facebook_access_key, 
					secret_key=facebook_secret_key
				)
				ads_config_obj.save()

			try:
				conf_obj = AdsConfigurations.objects.get(service_provider='Google')
				conf_obj.developer_token = google_developer_token
				conf_obj.client_id = google_client_id
				conf_obj.client_secret = google_client_secret
				conf_obj.refresh_token = google_refresh_token
				conf_obj.save()

			except Exception as exc:
				ads_config_obj = AdsConfigurations(service_provider='Google', 
					developer_token=google_developer_token, 
					client_id=google_client_id, 
					client_secret=google_client_secret, 
					refresh_token=google_refresh_token
				)
				ads_config_obj.save()

		messages.success(request, 'Configurations saved successfuly')
		return redirect('users:user-profile')