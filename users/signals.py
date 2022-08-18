from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwags):
	if created:
		print('run')
		try:
			user_profile = Profile(user=instance)
			user_profile.save()

		except Exception as ObjectExistsAlready:
			pass
			