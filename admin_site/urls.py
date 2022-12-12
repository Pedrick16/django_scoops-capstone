from django.urls import path
from admin_site import views
from django.conf import settings
from django.conf.urls.static import static



app_name = 'admin_site'
urlpatterns = [
    path('', views.dashboard_admin, name='dashboard'),
    path('list-inquiry/', views.list_inquiry, name='list_inquiry'),
    path('list-reseller/', views.list_reseller, name='list_reseller'),
    path('archive-reseller/<int:resellerid>/', views.archive_reseller, name='archive_reseller'),

    path('list-archive-reseller/', views.list_archive, name='list_archive'),
    path('retrieve-reseller/<int:resellerid>/', views.retrieve_reseller, name='retrieve_reseller'),



    path('send-email/<int:inquiryid>', views.send_email, name='send_email'),


  
    path('process/inquiry', views.process_inquiry, name='process_inquiry'),

    #adding reseller 
    path('adding-reseller/', views.add_reseller, name='add_reseller'),

   
    
    path('product/', views.list_products, name='list_product'),
    path('add-product/', views.add_product, name='add_product'),


    path('inventory/', views.inventory, name='inventory'),
    path('process-inventory/<int:productid>/', views.update_inventory, name='update_inventory'),

    path('pos/', views.pos ,name='pos'),

    path('minus-qty/<int:productid>/', views.minus_qty, name='minus_qty'),
    path('add-qty/<int:productid>/', views.add_qty ,name='add_qty'),

    path('pos/cancel/<int:productid>/', views.pos_cancel,name='pos_cancel'),

    path('pos/all-products/', views.all_products ,name='all_products'),
    path('cart/all-products/<int:productid>/', views.cart_products ,name='cart_products'),

    path('transaction-orders/', views.Transaction_orders ,name='transaction_orders'),

    path('reports/', views.reports ,name='reports'),

    path('search-reseller/', views.search_reseller, name='search_reseller'),
    path('search-product/', views.search_product, name='search_product'),
    path('search-inventory/', views.search_inventory, name='search_inventory'),
    path('search-transaction/', views.search_transaction, name='search_transaction'),



]