from django import forms
from commonuser.models import CommonUserModel
from django.core import validators


class CommonUserForm(forms.ModelForm):
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = CommonUserModel
        fields = ('phone_number',)
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder':'09121234567 مثال',}),
        }


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea','style': "height: 100px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class ConfirmationForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea(attrs={'id': 'code',}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])



class EmailForm(forms.Form):
    subject = forms.CharField()
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea','style': "height: 100px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
