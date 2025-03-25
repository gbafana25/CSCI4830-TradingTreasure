from django.urls import path, include
from . import views

urlpatterns = [
	path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name='profile')
]