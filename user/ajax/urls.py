from django.urls import path
from .views import *


urlpatterns = [
    #update user active url
    path('update-user-active/', update_user_active, name='update-user-active-ajax'),
    
    # update wallete status
    path('update-wallete-status/', update_wallet_status, name='update-wallet-status-ajax'),
]
