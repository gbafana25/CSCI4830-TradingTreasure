from django.shortcuts import render, redirect
from .forms import SignupForm, AddressForm, ProductForm
from .models import User, Address, Product
from django.shortcuts import get_object_or_404, redirect

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

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

def Item(request):
    return render(request, 'site_app/items.html', {})

def add_product(request):
    # Handle the form for adding a new product
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.owner = request.user  # Set the current user as the product owner
            new_product.save()
            return redirect('product_list')  # Redirect to the product list after saving
    else:
        form = ProductForm()

    return render(request, 'site_app/add_product.html', {'form': form})

def product_list(request):
    # Fetch all products from the database
    products = Product.objects.filter(is_bought=False)  # Filtder out the bought ones if you want to show only available products
    return render(request, 'site_app/items.html', {'products': products})
