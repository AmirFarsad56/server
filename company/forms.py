from django import forms
from company.models import TermsModel
from django.core import validators



class TermsForm(forms.ModelForm):
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta():
        model = TermsModel
        fields = ('terms_condition',)
        widgets = {
            'terms_condition': forms.Textarea(attrs={'class': 'materialize-textarea','style': "height: 100px"}),
        }


class TestForm(forms.Form):
    DatePicker = forms.CharField(widget =forms.TextInput(attrs={'type':'text' , 'id':'exampleInput3', 'data-mddatetimepicker':'true' ,'data-englishnumbe':'true' }))


class ContactUsForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'id': 'email'}),required=True)
    user_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name'}),required=True)
    user_phone = forms.CharField(widget=forms.TextInput(attrs={'id': 'phone_number'}),required=False)
    text = forms.CharField(widget=forms.TextInput(attrs={'id':'text','class': 'materialize-textarea','style': "height: 100px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class SportClubContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'name'}),required=True)
    sportclub_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'sportclub_name'}),required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'id': 'phone'}),required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'id':'address','class': 'materialize-textarea','style': "height: 80px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
