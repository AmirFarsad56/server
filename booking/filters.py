from booking.models import ContractModel
from django import forms
import django_filters


class ContractFilter(django_filters.FilterSet):
    total_price__gte = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    total_price__lte = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte')
    created_at_time__gte = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={'class':'timepicker'}),field_name='created_at_time', lookup_expr='gte')
    created_at_time__lte = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={'class':'timepicker'}),field_name='created_at_time', lookup_expr='lte')
    numbers__gte = django_filters.NumberFilter(field_name='numbers', lookup_expr='gte')
    numbers__lte = django_filters.NumberFilter(field_name='numbers', lookup_expr='lte')
    str_created_at_date = django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'mp-datepicker'}),field_name='str_created_at_date')

    class Meta:
        model = ContractModel
        fields = ['str_created_at_date',]
