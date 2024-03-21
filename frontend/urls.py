from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *
from user.email import password_reset, password_reset_confirm


urlpatterns = [
    path('ajax/', include('frontend.ajax.urls')),
    path('', home, name='home'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    
    path('mine/', mine, name='user_mine'),
    
    path('recharge/', recharge, name='user_recharge'),
    path('wallet/', wallet, name='user_wallet'),
    path('bank-details/', save_bankdetails, name='user_bank_save'),
    path('withdrowal/', withdrowal, name='user_withdrowal'),
    path('call-put/<int:market_id>/', call_put, name='call_put'),
    
    # Terms and Conditions
    path('terms-and-conditions/', tc, name="tc"),
    
    # About US
    path('about-us/', about_us, name="about_us"),
    path('team/', my_team, name="my_team"),
    
    # User Password
    path('password-reset/', password_reset, name='reset_user_password'),
    path('set-password/<slug:uid>/<slug:token>/', password_reset_confirm, name='confirm_reset_password'),
]
