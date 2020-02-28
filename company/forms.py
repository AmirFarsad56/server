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
