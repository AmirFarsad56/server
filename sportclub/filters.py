from sportclub.models import SportClubModel
import django_filters
from django import forms


class SportClubFilter(django_filters.FilterSet):
    sportclub_name = django_filters.CharFilter(widget=forms.TextInput(attrs={'id': 'sportclub_name',}),field_name='sportclub_name', lookup_expr='icontains')
    region = django_filters.CharFilter(widget=forms.TextInput(attrs={'id': 'region',}),field_name='region', lookup_expr='icontains')
    company_phone_number = django_filters.CharFilter(widget=forms.TextInput(attrs={'id': 'company_phone_number',}),field_name='company_phone_number', lookup_expr='icontains')
    serial_number = django_filters.CharFilter(widget=forms.TextInput(attrs={'id': 'serial_number',}))
    class Meta:
        model = SportClubModel
        fields = ('serial_number',)
