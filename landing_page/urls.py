from django.urls import path
from landing_page import views


app_name = 'landing_page'
urlpatterns = [
    # login process
    path('', views.landing_page, name='landing_site'),
    path('sign-in/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),

    
    #landing features
    path('inquiry/', views.inquiry_reseller, name='inquiry_reseller'),
]