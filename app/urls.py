from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


urlpatterns = [
        path('api/products/', views.get_products, name='get_products'),  # List all products
        path('api/products/<int:pk>/', views.get_product, name='get_product'),  # Get specific product
         
        path('api/brands/', views.get_brands, name='get_brands'),  # List all brands
        path('api/brands/<int:pk>/', views.get_brand, name='get_brand'),  # Get, update, or delete a specific brand
        
        path('api/check_auth_status/',views.check_auth_status,name='check_auth_status/'),
        
        path('api/signup/',views.signup,name='signup'),
        path('api/login/',views.login_view,name='login'),

        path('api/logout/',views.logout_view,name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)