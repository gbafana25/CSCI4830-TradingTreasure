from django.urls import path, include
from . import views

urlpatterns = [
	path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name='profile'),
    path('update_address', views.update_address, name='update_address'),
    path('Items', view.item, name='itmes'),
    path('add-product/', views.add_product, name='add_product')
]