from company.models import ReckoningModel
from django import forms
import django_filters


class ReckoningFilter(django_filters.FilterSet):
    money_transfered__gte = django_filters.NumberFilter(field_name='money_transfered', lookup_expr='gte')
    money_transfered__lte = django_filters.NumberFilter(field_name='money_transfered', lookup_expr='lte')
    transfered_at_time__gte = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={'class':'timepicker'}),field_name='transfered_at_time', lookup_expr='gte')
    transfered_at_time__lte = django_filters.TimeFilter(widget=forms.TimeInput(format='%H:%M',attrs={'class':'timepicker'}),field_name='transfered_at_time', lookup_expr='lte')
    str_transfered_at_date = django_filters.CharFilter(widget=forms.TextInput(attrs={'class':'mp-datepicker'}),field_name='str_transfered_at_date')

    class Meta:
        model = ReckoningModel
        fields = ['str_transfered_at_date',]
