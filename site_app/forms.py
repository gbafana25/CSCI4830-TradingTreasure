from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
	#username = forms.CharField()
	#password = forms.CharField()
	#email = forms.CharField()
	#location = forms.CharField()
	#phone_number = forms.IntegerField()
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "location", "phone_number")
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()