from django.shortcuts import render
from users.models import SubscriptionsDetails

def HomeView(request):
	print('User: ',request.user.pk)
	susbscriptions_obj = SubscriptionsDetails.objects.get(user_id=request.user)
	print('Subscriptions: ',susbscriptions_obj.get_package())
	context = {
		'title'	:	'Crunchscaled - Home',
		'susbscriptions_obj'	:	susbscriptions_obj,
	}
	return render(request, 'home.html', context)