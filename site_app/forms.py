from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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
   
    fields = ['name', 'price', 'category', 'owner', 'buyer_address', 'is_bought']
    widgets = {
        'category': forms.Textarea(attrs={'placeholder': 'Enter categories separated by semicolons'}),
        }

