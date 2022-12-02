from django.urls import path
from admin_site import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'admin_site'
urlpatterns = [
    path('', views.list_inquiry, name='list_inquiry'),
    path('list-reseller', views.list_reseller, name='list_reseller'),
    path('process/inquiry', views.process_inquiry, name='process_inquiry'),
    

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)    