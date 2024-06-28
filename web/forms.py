from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'phone_number', 'email', 'address', 'land_mark',
            'town_city', 'state', 'postcode_zip', 'country_name', 'payment_methode'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name', 'required': 'required'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'required'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Complete Address', 'required': 'required'}),
            'land_mark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Landmark', 'required': 'required'}),
            'town_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Town/City', 'required': 'required'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State', 'required': 'required'}),
            'postcode_zip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode/Zip', 'required': 'required'}),
            'country_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country', 'required': 'required'}),
            'payment_methode': forms.Select(attrs={'class': 'form-control', 'required': 'required'})
        }
