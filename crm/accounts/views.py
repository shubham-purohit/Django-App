from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def dashboard(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_orders = orders.count()
	total_customers = customers.count()
	delivered = orders.filter(status = "Delivered").count()
	pending = orders.filter(status = "Pending").count()

	context = {'orders': orders, 'customers': customers,
	 'total_orders' : total_orders, 'total_customers': total_customers,
	 'delivered' : delivered, 'pending' : pending}
	return render(request,'accounts/dashboard.html',context)

@login_required(login_url = 'login')
def product(request):
	products = Product.objects.all()
	return render(request,'accounts/product.html',{'products':products})

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def customer(request,cust_id):
	customer = Customer.objects.get(id=cust_id)
	orders = Order.objects.filter(customer = cust_id)
	total_orders = orders.count()
	orderFilter = OrderFilter(request.GET, queryset=orders)
	orders = orderFilter.qs
	context = {'customer': customer, 'orders': orders, 'total_orders': total_orders, 'orderFilter': orderFilter}
	return render(request,'accounts/customer.html', context)		

@login_required(login_url = 'login')
def create_order(request, cust_id):
	customer = Customer.objects.get(id=cust_id)
	OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product','status'), extra = 2)
	formset = OrderFormSet(instance=customer)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance = customer)
		print(formset.is_valid())
		if formset.is_valid():
			formset.save()
			print("Saved!!")
			return redirect('/')
		else:
			return redirect('/')	
	else:
		formset = OrderFormSet(queryset= Order.objects.none(),instance=customer)

	context = {'formset' : formset}
	return render(request, 'accounts/create_order.html', context)

@login_required(login_url = 'login')
def update_order(request, ord_id):
	order = Order.objects.get(id=ord_id)
	print(order)
	if request.method == 'POST':
		print(order)
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = OrderForm(instance=order)

	context = {'form' : form}
	return render(request, 'accounts/update_order.html', context)


@login_required(login_url = 'login')
def delete_order(request, ord_id):
	order = Order.objects.get(id=ord_id)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'order' : order}
	order = Order.objects.get(id=ord_id)
	order = Order.objects.get(id=ord_id)
	print(order)
	if request.method == 'POST':
		print(order)
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
	print(order)
	if request.method == 'POST':
		print(order)
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
	return render(request, 'accounts/delete_order.html', context)		


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def create_customer(request):

	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = CustomerForm()

	context = {'form' : form}


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	total_orders = orders.count()
	context = {'orders': orders, 'total_orders': total_orders,
				'delivered': delivered, 'pending': pending}
	return render(request, 'accounts/user.html', context)	


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def settings(request):
	context = {}
	return render(request, 'accounts/settings.html', context)


@unauthenticated_user
def loginUser(request):	
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			return redirect('userPage')
		else:
			messages.info(request, 'UserName or Password is incorrect')		
	
	context = {}
	return render(request, 'accounts/login.html', context)

@login_required(login_url = 'login')
def logoutUser(request):
	logout(request)
	return redirect('login')


@unauthenticated_user
def register(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username =  form.cleaned_data.get('username')

			group = Group.objects.get(name = 'customer')
			user.groups.add(group)

			Customer.objects.create(
				user = user,
				name = username,
				)

			messages.success(request, 'Account craeted for ' + username)
			return redirect('login')
	else:
		form = CreateUserForm()
	context = {'form': form}
	return render(request, 'accounts/register.html', context)	