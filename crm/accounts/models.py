from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	username = models.CharField(max_length=15, null=True)
	firstname = models.CharField(max_length=20, null=True)
	lastname = models.CharField(max_length=20, null=True)
	phone = models.CharField(max_length=10, null=True)
	email = models.CharField(max_length=30, null=True)
	address = models.CharField(max_length=60, null=True)
	profile_pic = models.ImageField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add = True, null=True)	

	def __str__(self):
		return self.user.username


class Tag(models.Model):

	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name



class Product(models.Model):
	CATEGORY = (
		('Indoor', 'Indoor'),
		('Outdoor', 'Outdoor')
		)


	name = models.CharField(max_length=200, null=True)
	price = models.FloatField()
	stock = models.PositiveIntegerField(default=0)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	product_pic = models.ImageField(null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add = True, null=True)
	tags = models.ManyToManyField(Tag)	

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
		('Pending', 'Pending'),
		('Out for delivery', 'Out for delivery'),
		('Delivered','Delivered')
		)

	customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
	date_created = 	models.DateTimeField(auto_now_add = True, null=True)
	notes = models.CharField(max_length=1000, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	completed = models.BooleanField(default=False, null=True, blank=True)

	def __str__(self):
		return self.customer.user.username + "_" + str(self.id)

	@property
	def get_total_items(self):
		orderItems = self.orderitem_set.all()
		total_items = sum([item.quantity for item in orderItems])
		return total_items

	@property
	def get_order_amount(self):
		orderItems = self.orderitem_set.all()
		order_amount = sum([item.get_total_price for item in orderItems])
		return order_amount
		
		



class OrderItem(models.Model):
	order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
	quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.order.customer.username + "_" + self.product.name

	@property	
	def get_total_price(self):
		return self.quantity * self.product.price	