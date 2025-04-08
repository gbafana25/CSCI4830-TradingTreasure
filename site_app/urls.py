from django.urls import path, include
from . import views

urlpatterns = [
	path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name='profile'),
    path('update_address', views.update_address, name='update_address'),
<<<<<<< Updated upstream
    path('Items', views.Item, name='items'),
    path('add-product/', views.add_product, name='add_product'),
=======
    path('page2/', views.page2, name="page2"),
    path('page3/', views.page3, name="page3"),
>>>>>>> Stashed changes
]