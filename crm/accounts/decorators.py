from django.shortcuts import redirect
from django.http import HttpResponse

def unauthenticated_user(view_function):
	def wrapper_func(request, *args, **kwrgs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_function(request, *args, **kwrgs)
	return wrapper_func	


def allowed_users(allowed_roles=[]):
	def decoartor(view_function):
		def wrapper_func(request, *args, **kwrgs):
			group = None
			if request.user.groups.exists():
				group =  request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_function(request, *args, **kwrgs)
			else:		
				return redirect('home')	
		return wrapper_func
	return decoartor