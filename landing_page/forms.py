from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':"username",
            'id':'username',
            'type':'text',
            'placeholder':'username',
            'maxlength':'25',
            'minlength':'6'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'email',
            'placeholder':'enter email',
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':"password1",
            'id':'password1',
            'type':'password',
            'placeholder':'password',
            'maxlength':'40',
            'minlength':'6'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':"password2",
            'id':'password2',
            'type':'password',
            'placeholder':'re-enter password',
            'maxlength':'40',
            'minlength':'6'
        })
        

    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )

    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control",'placeholder':'password'
    #         }
    #     )
    # )

    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control",'placeholder':'Re Enter password'
    #         }
    #     )
    # )

    # email = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )


    class Meta:
        model = User
        fields = ('username','email','password1','password2','role','status')
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)



