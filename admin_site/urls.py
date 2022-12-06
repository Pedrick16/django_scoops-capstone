from django.urls import path
from admin_site import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'admin_site'
urlpatterns = [
    path('', views.dashboard_admin, name='dashboard'),
    path('list-inquiry/', views.list_inquiry, name='list_inquiry'),
    path('list-reseller/', views.list_reseller, name='list_reseller'),

    path('search-reseller/', views.search_reseller, name='search_reseller'),
    path('search/product/', views.search_product, name='search_product'),
    path('search/product/', views.search_inventory, name='search_product'),

    path('archive-reseller/<int:resellerid>/', views.archive_reseller, name='archive_reseller'),
    path('process/inquiry', views.process_inquiry, name='process_inquiry'),

    #adding reseller 
    path('adding-reseller/', views.add_reseller, name='add_reseller'),

   
    
    path('product/', views.list_products, name='list_product'),

    path('inventory/', views.inventory, name='inventory'),
    path('process-inventory/<int:productid>/', views.update_inventory, name='update_inventory'),

    path('pos/', views.pos ,name='pos'),
    path('pos/cancel/<int:productid>/', views.pos_cancel,name='pos_cancel'),
    path('pos/compute/', views.pos_compute, name='pos_compute'),
    path('pos/all-products/', views.all_products ,name='all_products'),
    path('cart/all-products/<int:productid>', views.cart_products ,name='cart_products'),


    

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)    