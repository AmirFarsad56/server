from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserModel
from django.core import validators

class UserForm(UserCreationForm):
    '''form for creating a user'''


    terms = forms.BooleanField(
    error_messages={'required': 'You must accept terms and conditions'},
    )

    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta(UserCreationForm):
        model = UserModel
        fields = ('username','email','first_name',
                  'last_name','password1','password2')
        widgets = {
            'username': forms.TextInput(attrs={'id':'username','name':'username','onblur':'checkLength(this)'}),
            'email': forms.TextInput(attrs={'id':'email'}),
            'first_name': forms.TextInput(attrs={'id':'first_name'}),
            'password1': forms.TextInput(attrs={'id':'password1'}),
            'password2': forms.TextInput(attrs={'id':'password2'}),
        }


class TypesForm(forms.Form):

    commonusers = forms.BooleanField(required=False)
    masterusers = forms.BooleanField(required=False)
    sportclubs = forms.BooleanField(required=False)

    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class ForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder':'مثال 09123456789'}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea','style': "height: 100px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class EmailForm(forms.Form):
    subject = forms.CharField()
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea','style': "height: 100px"}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])


class UserUpdateForm(forms.ModelForm):
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta():
        model = UserModel
        fields = ('first_name','email',)
        widgets = {
            'email': forms.TextInput(attrs={'id':'email'}),
            'first_name': forms.TextInput(attrs={'id':'first_name'}),
        }


class SuperUserUpdateForm(forms.ModelForm):
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    def __init__(self, *args, **kwargs):
        super(SuperUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False


    class Meta():
        model = UserModel
        fields = ('first_name','last_name','email','picture')
        widgets = {
            'picture': forms.FileInput(attrs={}),
        }


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'current_password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'new_password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'confirm_password'}))
    Hfield = forms.CharField(required=False,widget =forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
