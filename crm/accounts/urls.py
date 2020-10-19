from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.register, name='register'),
	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name = 'logout'),

	path('', views.dashboard, name='home'),
	path('user/', views.userPage, name='userPage'),
	path('settings/', views.settings, name='settings'),
	path('products/', views.product, name='products'),
	path('customer/<str:cust_id>/', views.customer, name='customer'),
	path('create_order/<str:cust_id>', views.create_order, name='create_order'),
	path('update_order/<str:ord_id>', views.update_order, name='update_order'),
	path('delete_order/<str:ord_id>', views.delete_order, name='delete_order'),
	path('create_customer/', views.create_customer, name='create_customer'),
	path('create_product/', views.create_product, name = 'create_product'),
	path('update_product/<str:prod_id>', views.update_product, name = 'update_product'),
	path('delete_product/<str:prod_id>', views.delete_product, name = 'delete_product'),
	path('by_now/<str:prod_id>', views.buy_now, name='buy_now'),
	path('update_item/', views.update_item, name = 'update_item'),
	path('cart/', views.cart, name = 'cart'),

]