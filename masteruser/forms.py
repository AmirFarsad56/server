from django import forms
from masteruser.models import MasterUserModel
from django.core import validators


class MasterUserForm(forms.ModelForm):
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = MasterUserModel
        fields = ('phone_number',)
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder':'09121234567 مثال'}),
        }


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class EmailForm(forms.Form):
    subject = forms.CharField(widget=forms.Textarea)
    text = forms.CharField(widget=forms.Textarea)
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class MasterUserUpdateForm(forms.ModelForm):
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    def __init__(self, *args, **kwargs):
        super(MasterUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False
    class Meta():
        model = MasterUserModel
        fields = ('phone_number','picture')
        widgets = {
            'picture': forms.FileInput(attrs={}),
        }
