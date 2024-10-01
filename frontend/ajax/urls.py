from django.urls import path
from .views import *
from razor_pay.views import verify_payment
# from wepay.views import verify_payment_wepay, notify_payment_wepay


urlpatterns = [
    # call or put bid 
    path('call-put-bid/', call_put_bid, name='call-put-bid'),
    # path('recharge-using-rzp/', recharge, name='recharge_rzp'),
    path('recharge-using-wepay/', recharge_wepay, name='recharge_wepay'),
    path('verify-rzp-pay/', verify_payment, name='verify_rzp_payment'),
    # path('verify-wepay-pay/', verify_payment_wepay, name='verify_wepay_payment'),
    # path('notiify-wepay-pay/', notify_payment_wepay, name='notify_wepay_payment'),
]
