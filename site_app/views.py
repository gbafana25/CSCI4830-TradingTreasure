from django.shortcuts import render, redirect
from .forms import SignupForm, AddressForm, ProductForm
from .models import User, Address, Product
from django.http import HttpResponse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

import logging
log = logging.getLogger(__name__)

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
    return render(request, 'site_app/elements.html', {'profile': u, 'form': addr_form})


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
    #buy page
    products = Product.objects.filter(is_bought=False)
    product_list = []
    for p in products:
        product_list.append(p)
    paginator = Paginator(product_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'site_app/index.html', {
        'products': product_list, 
        'page_obj': page_obj
    })

def page2(request):
    #sell page
    #generic.html
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        log.debug(product_form)
        if product_form.is_valid():
            # right now just using the first line of the address to fetch the Address database object
            # Product buyer_address must be the database object
            line1 = product_form.cleaned_data['buyer_address'].split(',')[0]
            addr = Address.objects.get(address_line1=line1)
            p = Product(name=product_form.cleaned_data['name'], price=product_form.cleaned_data['price'], category=product_form.cleaned_data['category'], owner=request.user, buyer_address=addr, is_bought=False)
            p.save()
            redirect('/')
    else:
        product_form = ProductForm()
    return render(request, 'site_app/generic.html', {'form': product_form})

def page3(request):
    #accounts page
    #elements.html



    return render(request, 'site_app/elements.html', {})

def buy_item(request, id):
    prod = Product.objects.get(id=id)
    return render(request, 'site_app/buy_item.html', {'prod': prod})