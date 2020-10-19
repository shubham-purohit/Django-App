from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import json

from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm, ProductForm
from .filters import OrderFilter, ProductFilter
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
	productFilter = ProductFilter(request.GET, queryset=products)
	
	products = productFilter.qs
	context = {'products':products, 'productFilter' : productFilter}
	return render(request,'accounts/products.html',context)


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
@allowed_users(allowed_roles = ['admin'])
def create_product(request):
	if request.method == 'POST':
		form = ProductForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('products')
		else:
			messages.info(request, 'Incorrect data. Please, refill the details.')	
	else:
		form = ProductForm()

	context = {'form' : form}
	return render(request, 'accounts/create_product.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def update_product(request, prod_id):
	product = Product.objects.get(id=prod_id)
	if request.method == 'POST':
		print(request.FILES)
		form = ProductForm(request.POST,request.FILES,instance=product)
		if form.is_valid():
			print(form.cleaned_data)
			form.save()
			return redirect('products')
	else:
		form = ProductForm(instance=product)

	context = {'form' : form, 'product' : product}
	return render(request, 'accounts/update_product.html', context)	



@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def delete_product(request, prod_id):
	product = Product.objects.get(id=prod_id)
	if request.method == 'POST':
		product.delete()
		return redirect('products')
	context = {'product' : product}

	return render(request, 'accounts/delete_product.html', context)	



@login_required(login_url = 'login')
def create_order(request, cust_id):
	customer = Customer.objects.get(id=cust_id)
	OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product','status'), extra = 2)
	formset = OrderFormSet(instance=customer)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance = customer)
		if formset.is_valid():
			formset.save()
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
	if request.method == 'POST':
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
	customer = request.user.customer
	if request.method == 'POST':
		form = CustomerForm(request.POST,request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('settings')
	else:
		form = CustomerForm(instance = customer)

	context = {'form' : form}
	return render(request, 'accounts/settings.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def buy_now(request, prod_id):	
	product = Product.objects.get(id=prod_id)
	context = {'product': product}
	return render(request, 'accounts/buy_now.html', context)

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

			messages.success(request, 'Account craeted for ' + username)
			return redirect('login')
	else:
		form = CreateUserForm()
	context = {'form': form}
	return render(request, 'accounts/register.html', context)


def update_item(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer = request.user.customer, completed=False)
	orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

	if action == 'add':
		orderItem.quantity += 1
	elif action == 'remove':
		orderItem.quantity -= 1
	elif action == 'delete':
		orderItem.quantity = 0	
	
	orderItem.save()

	if orderItem.quantity == 0:
		orderItem.delete()		

	return JsonResponse("Item was added", safe=False);


def cart(request):
	try:
		order = Order.objects.get(customer=request.user.customer, completed=False)
		orderItems = order.orderitem_set.all()
		context = {'orderItems' : orderItems, 'order' : order}
		print(context)
	except:
		print("Exception")
		context = {}	
	return render(request, 'accounts/cart.html', context)			