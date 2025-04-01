from django.shortcuts import render, redirect
from .forms import ItemForm
from .models import Item
from django.shortcuts import get_object_or_404, redirect
from .forms import SignupForm, AddressForm
from .models import User, Address
from django.http import HttpResponse

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items})


def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form})

def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'items/item_confirm_delete.html', {'item': item})

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def signup(request):
    if request.method == 'POST':
        signupform = SignupForm(request.POST)

        if signupform.is_valid():
            #print(signupform.cleaned_data)
            new_user = User.objects.create_user(signupform.cleaned_data['username'], signupform.cleaned_data['email'], signupform.cleaned_data['password'])
            new_user.location = signupform.cleaned_data['location']
            new_user.phone_number = signupform.cleaned_data['phone_number']
            new_user.save()
            #new_user = signupform.save()
            login(request, new_user)
            addr_form = AddressForm()
            return render(request, 'site_app/profile.html', {'profile': new_user, 'form': addr_form})
        
    else:
        signupform = SignupForm()
    return render(request, 'site_app/signup.html', {'form': signupform})

@login_required
def profile(request):
    u = request.user
    addr_form = AddressForm()
    return render(request, 'site_app/profile.html', {'profile': u, 'form': addr_form})

@login_required
def update_address(request):
    u = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        addr_form = AddressForm(request.POST)
        if addr_form.is_valid():
            addr = Address.objects.create(address_line1=addr_form.cleaned_data['address_line1'], address_line2=addr_form.cleaned_data['address_line2'], city=addr_form.cleaned_data['city'], state=addr_form.cleaned_data['state'], zip_code=addr_form.cleaned_data['zip_code'])
            u.address = addr
            u.save()
    else:
        addr_form = AddressForm()

    return render(request, 'site_app/profile.html', {'profile': u, 'form': addr_form})

def home(request):
    return render(request, 'site_app/home.html', {})
