from django import forms 
from .models import Order 



class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order 
        fields = ['full_name', 'phone','address', 'town', 'region']

        widgets = {
            'full_name':forms.TextInput(attrs={
                'class':'w-full rounded-lg p-3 border border-gray',
                'placeholder':'Full Name',

            }),

            'phone': forms.TextInput(attrs={
                'class': 'w-full rounded-lg p-3 border border-gray',
                'placeholder': "e.g 024xxxxxxx",
                
            }),

            'address': forms.TextInput(attrs={
                'class': 'w-full rounded-lg p-3 border border-gray',
                'placeholder': "Address",
            }),

            'town': forms.TextInput(attrs={
                'class': 'w-full rounded-lg p-3 border border-gray',
                'placeholder': "City/Town/Village",
            }),

            'region': forms.TextInput(attrs={
                'class': 'w-full rounded-lg p-3 border border-gray',
                'placeholder': "Region",
            })
        }


