from django.urls import path
from .views import *
from razor_pay.views import verify_payment


urlpatterns = [
    # call or put bid 
    path('call-put-bid/', call_put_bid, name='call-put-bid'),
    path('recharge-using-rzp/', recharge, name='recharge_rzp'),
    path('verify-rzp-pay/', verify_payment, name='verify_rzp_payment'),
]
