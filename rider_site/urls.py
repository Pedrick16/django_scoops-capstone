from django.urls import path
from rider_site import views

app_name = 'rider_site'
urlpatterns = [
    path('', views.dashboard, name='dashboard_rider'),
    path('orders-reseller', views.deliver_orders, name='deliver_orders'),
    path('orders-completed/<int:orderid>/', views.orders_completed, name='orders_completed')
]