from django.urls import path
from reseller_site import views

app_name = 'reseller_site'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.transaction_orders, name='transaction_orders'),
    path('transaction-view/<int:id>/', views.transaction_view, name='transaction_view'),
    path('cart/', views.cart_reseller, name='cart_reseller'),
    path('checkout/', views.checkout, name='checkout'),

]