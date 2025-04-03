from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('site_app.urls')),
    path('item/new/', views.create_item, name='create_item'),
    path('item/<int:pk>/edit/', views.update_item, name='update_item'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete_item')
]