from django.urls import path, include
from . import views

urlpatterns = [
	path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name="home"),
    #path('<int:page>/', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name='profile'),
    path('update_address', views.update_address, name='update_address'),
    path('page2/', views.page2, name="page2"),
    path('page3/', views.page3, name="page3"),
    path('buy-item/<uuid:id>/', views.buy_item, name="buy-item"),
    path('place-order/<uuid:id>/', views.place_order, name="place-order"),
    path('message-owner/<uuid:id>/', views.message_owner, name="message-owner"),
    path('confirm-order/<uuid:id>/', views.confirm_order, name="confirm-order"),
    path('pay/', views.PaymentCheckoutView.as_view(), name='pay'),
    path('pay_success', views.SuccessView.as_view(), name='pay_success'),
    path('pay_cancel', views.CancelView.as_view(), name='pay_cancel'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
]