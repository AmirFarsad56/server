from django import forms
from django.core import validators


class NumberForm(forms.Form):
    numbers = forms.IntegerField()
    range_start = forms.CharField(widget=forms.TextInput(attrs={'class':'mp-datepicker'}),required = True)
    range_end = forms.CharField(widget=forms.TextInput(attrs={'class':'mp-datepicker'}),required = True)

    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
