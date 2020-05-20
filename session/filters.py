from session.models import SessionModel
from django import forms
import django_filters


class SessionFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(widget=forms.TextInput(attrs={"style":"direction:rtl; text-align:right; color:#d4af37; font-family: 'Lalezar', cursive;",'placeholder': 'قیمت سانس کمتر از (تومان)','id': 'price__gte',}),field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(widget=forms.TextInput(attrs={"style":"direction:rtl; text-align:right; color:#d4af37; font-family: 'Lalezar', cursive;",'placeholder': 'قیمت سانس بیشتز از (تومان)','id': 'price__lte',}),field_name='price', lookup_expr='lte')
    time__gte = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={"style":"direction:rtl; text-align:right; color:#d4af37; font-family: 'Lalezar', cursive;",'placeholder': 'ساعت شروع سانس بعد از','id': 'time__gte','class':'timepicker'}),field_name='time', lookup_expr='gte')
    time__lte = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={"style":"direction:rtl; text-align:right; color:#d4af37; font-family: 'Lalezar', cursive;",'placeholder': 'ساعت شروع سانس قبل از','id': 'time__lte','class':'timepicker'}),field_name='time', lookup_expr='lte')
    discount_percentage__gte = django_filters.NumberFilter(widget=forms.TextInput(attrs={"style":"direction:rtl; text-align:right; color:#d4af37; font-family: 'Lalezar', cursive;",'placeholder': 'درصد تخفیف کمتر از','id': 'discount_percentage__gte',}),field_name='discount_percentage', lookup_expr='gte')
    discount_percentage__lte = django_filters.NumberFilter(widget=forms.TextInput(attrs={"style":"direction:rtl; text-align:right; color:#d4af37; font-family: 'Lalezar', cursive;",'placeholder': 'درصد تخفیف بیشتر از','id': 'discount_percentage__lte',}),field_name='discount_percentage', lookup_expr='lte')
    day_str = django_filters.CharFilter(widget=forms.TextInput(attrs={"style":"direction:rtl; text-align:right; color:#d4af37; font-family: 'Lalezar', cursive;",'placeholder': 'روز سانس','type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),field_name='day_str')
    duration = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={"style":"direction:rtl; text-align:right; color:#d4af37; font-family: 'Lalezar', cursive;",'placeholder': 'طول سانس','id': 'duration','class':'timepicker'}),field_name='duration',)

    class Meta:
        model = SessionModel
        fields = ['is_booked','is_ready',]
