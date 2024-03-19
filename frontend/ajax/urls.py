from django.urls import path
from .views import *


urlpatterns = [
    # call or put bid 
    path('call-put-bid/', call_put_bid, name='call-put-bid'),
]
