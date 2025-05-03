from django.shortcuts import render, redirect
from .forms import SignupForm, AddressForm, ProductForm, StripePaymentForm, MessageSellerForm
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
    return render(request, 'site_app/elements.html', {'profile': u, 'form': addr_form})


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

            return redirect('/')
    else:
        product_form = ProductForm()

    return render(request, 'site_app/generic.html', {'form': product_form})

@login_required
def page3(request):
    account_orders = Order.objects.filter(seller=request.user)
    return render(request, 'site_app/elements.html', {'orders': account_orders})


@login_required
def buy_item(request, id):
    prod = Product.objects.get(id=id)
    form = StripePaymentForm(initial={'product_id': prod.id})
    msgform = MessageSellerForm()
    return render(request, 'site_app/buy_item.html', {'prod': prod, 'stripe_form': form, 'msgform': msgform})

@login_required
def message_owner(request, id):
    if request.method == 'POST':
        mform = MessageSellerForm(request.POST)
        if mform.is_valid():
            prod = Product.objects.get(id=id)
            send_mail(
            "Message from "+request.user.username+" - Trading Treasure",
            mform.cleaned_data['message'],
            "tradingtreasure@example.com",
            [prod.owner.email],
            fail_silently=False
        )
        form = MessageSellerForm()
        return render(request, 'site_app/buy_item.html', {'prod': prod, 'msgform': form})
    else:
        form = MessageSellerForm()
        return render(request, 'site_app/buy_item.html', {'prod': prod, 'msgform': form})

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

    return home(request)


# Stripe payment logic
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class PaymentCheckoutView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': product.name},
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            #success_url='http://localhost:8000/pay_success?id='+str(product_id),
            success_url=request.build_absolute_uri(reverse('pay_success')+"?id="+str(product_id)),
            cancel_url=request.build_absolute_uri(reverse('pay_cancel')),
        )
        return redirect(checkout_session.url, code=303)


class SuccessView(View):
    template_name = 'site_app/payment_success.html'
    def get(self, request):
        prod_id = request.GET.get("id")
        product = Product.objects.get(id=prod_id)
        order_obj = Order.objects.create(
            product=product,
            buyer=request.user,
            seller=product.owner,
            buyer_address=request.user.address
        )
        product.is_bought = True
        product.save()

        send_mail(
            "Product purchased - Trading Treasure",
            f"Your product {product.name} has been purchased by {request.user.username} for ${product.price}",
            "tradingtreasure@example.com",
            [order_obj.seller.email],
            fail_silently=False
        )
        send_mail(
            "Product purchased - Trading Treasure",
            f"You purchased {product.name} for ${product.price}",
            "tradingtreasure@example.com",
            [request.user.email],
            fail_silently=False
        )

        return redirect('/')


class CancelView(TemplateView):
    template_name = 'site_app/payment_cancel.html'


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print('✅ Payment succeeded for session:', session['id'])

    return JsonResponse({'status': 'success'}, status=200)