from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def signup(request):
    if request.method == 'POST':
        signupform = SignupForm(request.POST)

        if signupform.is_valid():
            #print(signupform.cleaned_data)
            #new_user = User.objects.create_user(signupform.cleaned_data['username'], signupform.cleaned_data['email'], signupform.cleaned_data['password'])
            #new_user.location = signupform.cleaned_data['location']
            #new_user.phone_number = signupform.cleaned_data['phone_number']
            # TODO: set location, phone number, and address
            
            new_user = signupform.save()
            login(request, new_user)
            #redirect('/')
        
    else:
        signupform = SignupForm()
    return render(request, 'site_app/signup.html', {'form': signupform})

@login_required
def profile(request):
    u = request.user
    return render(request, 'site_app/profile.html', {'profile': u})

def home(request):
    return render(request, 'site_app/home.html', {})