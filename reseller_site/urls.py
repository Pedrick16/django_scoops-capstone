from django.urls import path
from reseller_site import views

app_name = 'reseller_site'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.orders_reseller, name='orders_reseller'),
    path('cart/', views.cart_reseller, name='cart_reseller'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile-reseller/', views.profile_reseller, name='profile_reseller'),
]