from django import forms
from commonuser.models import CommonUserModel
from django.core import validators


class CommonUserForm(forms.ModelForm):
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    def __init__(self, *args, **kwargs):
        super(CommonUserForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

    class Meta:
        model = CommonUserModel
        fields = ('phone_number','picture')
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder':'09121234567 مثال',}),
        }


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea','style': "height: 100px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class ConfirmationForm(forms.Form):
    code = forms.CharField()
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])



class EmailForm(forms.Form):
    subject = forms.CharField()
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea','style': "height: 100px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class CommonUserUpdateForm(forms.ModelForm):
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    def __init__(self, *args, **kwargs):
        super(CommonUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False

    class Meta():
        model = CommonUserModel
        fields = ('phone_number','picture')
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder':'09121234567 مثال',}),
            'picture': forms.FileInput(attrs={}),
        }
