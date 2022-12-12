from django.urls import path
from landing_page import views


app_name = 'landing_page'
urlpatterns = [
    # login process
    
    path('', views.landing_page, name='landing_site'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/', views.registerUser, name='register_user'),

    #landing features
    path('inquiry/', views.inquiry_reseller, name='inquiry_reseller'),


    # admin view site
    # staff view site
    path('staff-dashboard/', views.dashboard_staff, name='dashboard_staff'),



]