from django_filters import FilterSet, DateFilter, CharFilter
from .models  import *

class OrderFilter(FilterSet):
	start_time = DateFilter(field_name='date_created', lookup_expr='gte')
	end_time = DateFilter(field_name='date_created', lookup_expr='lte')
	notes = CharFilter(field_name='notes', lookup_expr='icontains')
	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'date_created']