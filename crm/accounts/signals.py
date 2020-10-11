from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .models import Customer

def customerProfile(sender, instance, created, **kwrgs):
	if created:
		group = Group.objects.get(name = 'customer')
		instance.groups.add(group)

		Customer.objects.create(
			user = instance,
			name = instance.username,
			)
		print("Profile Created!!")

post_save.connect(customerProfile, sender=User)		