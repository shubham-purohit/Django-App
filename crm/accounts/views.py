from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CustomerForm
from .filters import OrderFilter

# Create your views here.
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

def product(request):
	products = Product.objects.all()
	return render(request,'accounts/product.html',{'products':products})

def customer(request,cust_id):
	customer = Customer.objects.get(id=cust_id)
	orders = Order.objects.filter(customer = cust_id)
	total_orders = orders.count()
	orderFilter = OrderFilter(request.GET, queryset=orders)
	orders = orderFilter.qs
	context = {'customer': customer, 'orders': orders, 'total_orders': total_orders, 'orderFilter': orderFilter}
	return render(request,'accounts/customer.html', context)		

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

def delete_order(request, ord_id):
	order = Order.objects.get(id=ord_id)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'order' : order}
	return render(request, 'accounts/delete_order.html', context)		

def create_customer(request):

	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = CustomerForm()

	context = {'form' : form}
	return render(request, 'accounts/create_customer.html', context)