import django_filters
from django_filters import CharFilter

from .models import *


class OrderFilter(django_filters.FilterSet):
    note = CharFilter(field_name="note", lookup_expr="icontains")
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer','date_created']


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['User','date_created','profile_pic']