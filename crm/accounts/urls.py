from django.urls import path
from . import views

urlpatterns = [
	path('', views.dashboard, name='home'),
	path('products/', views.product, name='products'),
	path('customer/<str:cust_id>/', views.customer, name='customer'),
	path('create_order/<str:cust_id>', views.create_order, name='create_order'),
	path('update_order/<str:ord_id>', views.update_order, name='update_order'),
	path('delete_order/<str:ord_id>', views.delete_order, name='delete_order'),
	path('create_customer/', views.create_customer, name='create_customer'),

]