from django import forms
from session.models import SessionModel
from django.core import validators


class DaysForm(forms.Form):
    last_day = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = False)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class DaysForm_2(forms.Form):
    first_day = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    last_day = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class TimesForm(forms.Form):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M',attrs={'id':'start_time','type':'text','class':'timepicker'}),required = False)
    duration = forms.TimeField(widget=forms.TimeInput(format='%H:%M',attrs={'id':'duration','class':'timepicker'}), required = False)
    stop_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M',attrs={'id':'stop_time','class':'timepicker'}), required = False)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class PriceForm(forms.Form):
    range_start = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    range_end = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    price = forms.IntegerField(required = True)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class SessionDeleteForm(forms.Form):
    range_start = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    range_end = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class LastDataSetForm(forms.Form):
    first_day = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class DiscountPercentageForm(forms.Form):
    range_start = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    range_end = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    discount_percentage = forms.IntegerField(widget=forms.TextInput(attrs={'id':'discount_percentage'}),required = True)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class StatusForm(forms.Form):
    range_start = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    range_end = forms.CharField(widget=forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumber':'true', 'autocomplete':'off'}),required = True)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
