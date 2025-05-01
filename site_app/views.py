from django.shortcuts import render, redirect
from .forms import SignupForm, AddressForm, ProductForm, MessageOwnerForm, StripePaymentForm

from .models import User, Address, Product, Order
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail

import stripe


def signup(request):
    if request.method == 'POST':
        signupform = SignupForm(request.POST)

        if signupform.is_valid():
            new_addr = Address.objects.create(
                address_line1=signupform.cleaned_data['address_line1'],
                address_line2=signupform.cleaned_data['address_line2'],
                city=signupform.cleaned_data['city'],
                state=signupform.cleaned_data['state'],
                zip_code=signupform.cleaned_data['zip_code']
            )
            new_addr.save()

            new_user = User.objects.create_user(
                signupform.cleaned_data['username'],
                signupform.cleaned_data['email'],
                signupform.cleaned_data['password']
            )
            new_user.location = signupform.cleaned_data['location']
            new_user.phone_number = signupform.cleaned_data['phone_number']
            new_user.address = new_addr
            new_user.save()

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
    account_orders = Order.objects.filter(seller=request.user.id)
    return render(request, 'site_app/elements.html', {'profile': u, 'form': addr_form, 'orders': account_orders})


@login_required
def update_address(request):
    u = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        addr_form = AddressForm(request.POST)
        if addr_form.is_valid():
            addr = Address.objects.create(
                address_line1=addr_form.cleaned_data['address_line1'],
                address_line2=addr_form.cleaned_data['address_line2'],
                city=addr_form.cleaned_data['city'],
                state=addr_form.cleaned_data['state'],
                zip_code=addr_form.cleaned_data['zip_code']
            )
            u.address = addr
            u.save()
            return home(request)
    else:
        addr_form = AddressForm()

    return render(request, 'site_app/profile.html', {'profile': u, 'form': addr_form})


def home(request):
    products = Product.objects.filter(is_bought=False)
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'site_app/index.html', {
        'products': products,
        'page_obj': page_obj
    })


def page2(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            line1 = product_form.cleaned_data['buyer_address'].split(',')[0]
            addr = Address.objects.filter(address_line1=line1).first()

            p = Product.objects.create(
                name=product_form.cleaned_data['name'],
                price=product_form.cleaned_data['price'],
                category=product_form.cleaned_data['category'],
                owner=request.user,
                buyer_address=addr,
                is_bought=False
            )
            p.save()

            send_mail(
                "Product listed - Trading Treasure",
                f"Your product {p.name} has been listed for ${p.price}",
                "tradingtreasure@example.com",
                [request.user.email],
                fail_silently=False
            )
            return home(request)
    else:
        product_form = ProductForm()

    return render(request, 'site_app/generic.html', {'form': product_form})


def page3(request):
    account_orders = Order.objects.filter(buyer=request.user)
    return render(request, 'site_app/elements.html', {'orders': account_orders})


@login_required
def buy_item(request, id):
    prod = Product.objects.get(id=id)
    form = MessageOwnerForm()
    return render(request, 'site_app/buy_item.html', {'prod': prod, 'form': form})
    #form = StripePaymentForm(initial={'product_id': prod.id})
    return render(request, 'site_app/buy_item.html', {'prod': prod, 'stripe_form': form})


@login_required
def place_order(request, id):
    prod = Product.objects.get(id=id)
    order_obj = Order.objects.create(
        product=prod,
        buyer=request.user,
        seller=prod.owner,
        buyer_address=request.user.address
    )
    prod.is_bought = True
    prod.save()

    send_mail(
        "Product purchased - Trading Treasure",
        f"Your product {prod.name} has been purchased by {request.user.username} for ${prod.price}",
        "tradingtreasure@example.com",
        [order_obj.seller.email],
        fail_silently=False
    )
    send_mail(
        "Product purchased - Trading Treasure",
        f"You purchased {prod.name} for ${prod.price}",
        "tradingtreasure@example.com",
        [request.user.email],
        fail_silently=False
    )
    
@login_required
def message_owner(request, id):
    if request.method == 'POST':
        mform = MessageOwnerForm(request.POST)
        if mform.is_valid():
            prod = Product.objects.get(id=id)
            send_mail(
            "Message from "+request.user.username+" - Trading Treasure",
            mform.cleaned_data['message'],
            "tradingtreasure@example.com",
            [prod.owner.email],
            fail_silently=False
        )
        form = MessageOwnerForm()
        return render(request, 'site_app/buy_item.html', {'prod': prod, 'form': form})
    else:
        form = MessageOwnerForm()
        return render(request, 'site_app/buy_item.html', {'prod': prod, 'form': form})
    
@login_required
def confirm_order(request, id):
    order = Order.objects.get(id=id)
    send_mail(
        "Order confirmation from "+request.user.username+" - Trading Treasure",
        "Order confirmation for "+order.product.name,
        "tradingtreasure@example.com",
        [order.buyer.email],
        fail_silently=False
    )
    order.delete()
    return profile(request)
