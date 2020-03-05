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
    email = forms.CharField(required=True)
    user_name = forms.CharField(required=True)
    user_phone = forms.CharField(required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea','style': "height: 100px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
