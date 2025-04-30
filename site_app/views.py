from django.shortcuts import render, redirect
from .forms import SignupForm, AddressForm, ProductForm
from .models import User, Address, Product, Order
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.views import View

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

import stripe
import logging
#log = logging.getLogger(__name__)

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
            return render(request, 'site_app/elements.html', {'profile': new_user, 'form': addr_form})
        
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
            home(request)
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
        #log.debug(product_form)
        if product_form.is_valid():
            # right now just using the first line of the address to fetch the Address database object
            # Product buyer_address must be the database object
            line1 = product_form.cleaned_data['buyer_address'].split(',')[0]
            print(line1)
            addr = Address.objects.filter(address_line1=line1)
           # print(addr)
            p = Product(name=product_form.cleaned_data['name'], price=product_form.cleaned_data['price'], category=product_form.cleaned_data['category'], owner=request.user, buyer_address=addr[0], is_bought=False)
            p.save()
            home(request)
    else:
        product_form = ProductForm()
    return render(request, 'site_app/generic.html', {'form': product_form})

def page3(request):
    #accounts page
    #elements.html
    account_orders = Order.objects.filter(buyer=request.user)

    return render(request, 'site_app/elements.html', {'orders': account_orders})

@login_required
def buy_item(request, id):
    prod = Product.objects.get(id=id)
    return render(request, 'site_app/buy_item.html', {'prod': prod})

@login_required
def place_order(request, id):
    prod = Product.objects.get(id=id)
    order_obj = Order.objects.create(product=prod, buyer=request.user, seller=prod.owner, buyer_address=request.user.address)
    prod.is_bought = True
    prod.save()
    return home(request)

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://localhost:8000"
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data':{
                            'currency': 'usd',
                            'unit_amount': 2000,
                            'product_data': {
                                'name': 'Trading Treasure Item',
                                },
                            },
                        'quantity': 1,
                        },
                    ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
                )
        return JsonResponse({'id': checkout_session.id})
