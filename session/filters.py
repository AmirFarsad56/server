from session.models import SessionModel
from django import forms
import django_filters


class SessionFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    time__gte = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={'class':'timepicker'}),field_name='time', lookup_expr='gte')
    time__lte = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={'class':'timepicker'}),field_name='time', lookup_expr='lte')
    discount_percentage__gte = django_filters.NumberFilter(field_name='discount_percentage', lookup_expr='gte')
    discount_percentage__lte = django_filters.NumberFilter(field_name='discount_percentage', lookup_expr='lte')
    day_str = django_filters.CharFilter(widget=forms.TextInput(attrs={ 'type':'text', 'id':'datepicker',}),field_name='day_str')
    duration = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={'class':'timepicker'}),field_name='duration',)

    class Meta:
        model = SessionModel
        fields = ['is_booked','is_ready',]
