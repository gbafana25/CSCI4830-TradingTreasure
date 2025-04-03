from django import forms
from .models import Item
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Product

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price']

class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.CharField()
    location = forms.CharField()
    phone_number = forms.IntegerField()

class AddressForm(forms.Form):
        address_line1 = forms.CharField()
        address_line2 = forms.CharField()
        city = forms.CharField()
        state = forms.CharField()
        zip_code = forms.IntegerField()

        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category']  # You can customize the fields as needed
