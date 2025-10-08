from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(AuthenticationForm):
    class Meta:
        model = User 
        fields = ['username', 'password']



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password1', 'password2']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class':'rounded-md p-2 text-gray-800 w-70',
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class':'rounded-md p-2 text-gray-800 w-70',
    }))

    region = forms.CharField(widget=forms.TextInput(attrs={
        'class':'rounded-md p-2 text-gray-800 w-70',
    }))

    town = forms.CharField(widget=forms.TextInput(attrs={
        'class':'rounded-md p-2 text-gray-800 w-70',
    }))

    gender = forms.CharField(widget=forms.Select(choices=Profile.GENDER,attrs={
        'class':'rounded-md p-2 text-gray-800 w-70',
    }))

    profile_image = forms.ImageField(
    widget=forms.FileInput(attrs={
        'class': 'text-gray-800 rounded-md border border-gray-300 w-70 text-white'
    })
)


