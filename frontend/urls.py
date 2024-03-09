from django.urls import path, include
from .views import *


urlpatterns = [
    # path('ajax/', include('frontend.ajax.urls')),
    path('', home, name='home'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('mine/', mine, name='user_mine'),
    path('recharge/', recharge, name='user_recharge'),
    path('wallet/', wallet, name='user_wallet'),
]
