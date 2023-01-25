from django.urls import path
from reseller_site import views

app_name = 'reseller_site'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.transaction_orders, name='transaction_orders'),
    path('add-to-cart/', views.add_cart, name='add_cart'),

    path('minus-qty/<int:productid>/', views.minus_qty, name='minus_qty'),
    path('add-qty/<int:productid>/', views.add_qty ,name='add_qty'),
    path('pos/cancel/<int:productid>/', views.cart_cancel,name='cart_cancel'),


    path('transaction-view/<int:id>/', views.transaction_view, name='transaction_view'),
    path('cart/', views.cart_reseller, name='cart_reseller'),
    path('checkout/', views.checkout, name='checkout'),

]