from django.urls import path
from admin_site import views
from django.conf.urls.static import static



app_name = 'admin_site'
urlpatterns = [
    path('', views.dashboard_admin, name='dashboard'),
    path('list-inquiry/', views.list_inquiry, name='list_inquiry'),
    path('list-reseller/', views.list_reseller, name='list_reseller'),
    path('archive-reseller/<int:resellerid>/', views.archive_reseller, name='archive_reseller'),

    path('settings_profile/', views.settings_profile, name='settings_profile'),
    path('add_profile/', views.add_profile, name='add_profile'),
    path('update_profile/<int:profileid>', views.update_profile, name='update_profile'),
    path('My-profile/', views.my_profile, name='my_profile'),



    path('list-archive-reseller/', views.list_archive, name='list_archive'),
    path('retrieve-reseller/<int:id>/', views.retrieve_reseller, name='retrieve_reseller'),



    path('send-email/', views.send_email, name='send_email'),



    path('process/inquiry', views.process_inquiry, name='process_inquiry'),

    #adding reseller 
    path('adding-reseller/', views.add_reseller, name='add_reseller'),

    path('product/', views.list_products, name='list_product'),
    path('view-product/<int:productid>/', views.view_product, name='view_product'),
    path('add-product/', views.add_product, name='add_product'),


    path('inventory/', views.inventory, name='inventory'),
    path('view-inventory/', views.view_inventory, name='view_inventory'),
   
    path('update-inventory/<int:productid>/', views.update_inventory, name='update_inventory'),

    path('pos/', views.pos ,name='pos'),
    path('pos-receipt/', views.pos_receipt ,name='pos_receipt'),
    path('settings-receipt/', views.Click_receipt ,name='click_receipt'),
    
    path('pos/add-receipt/', views.pos_addreceipt ,name='add_receipt'),
    path('pos/receipt-process/', views.pos_receipt_process ,name='receipt_process'),

    path('minus-qty/<int:productid>/', views.minus_qty, name='minus_qty'),
    path('add-qty/<int:productid>/', views.add_qty ,name='add_qty'),

    path('pos/cancel/<int:productid>/', views.pos_cancel,name='pos_cancel'),


    path('pos/all-products/', views.all_products ,name='all_products'),
    path('cart/all-products/<int:productid>/', views.cart_products ,name='cart_products'),
    path('transaction-orders/pending', views.Transaction_orders, name='transaction_orders'),
    path('transaction-orders/process-out-for-delivery', views.delivery_process, name='delivery_process'),

    path('transaction-orders/out for shipping', views.Transaction_outshipping, name='transaction_outshipping'),

    path('transaction-orders/completed', views.Transaction_completed, name='transaction_completed'),
    path('transaction-orders/process-completed', views.completed_process, name='completed_process'),

    path('transaction-orders/decline', views.Transaction_decline, name='transaction_decline'),
    path('transaction-view/<int:id>/', views.transaction_view, name='transaction_view'),
 
    path('search-reseller/', views.search_reseller, name='search_reseller'),
    path('search-product/', views.search_product, name='search_product'),
    path('search-inventory/', views.search_inventory, name='search_inventory'),
    path('search-transaction/', views.search_transaction, name='search_transaction'),
    path('search/activity-log/', views.search_actlog, name='search_act-log'),

    path('reports/activity-log/', views.report_actlog, name='report_actlog'),
    # path('reports-sales/', views.report_sales, name='report_sales'),

    path('register/<int:inquiryid>/', views.register, name='register'),
    path('viewing-pic/<int:id>/', views.view_pic, name='viewing_pic'),
]