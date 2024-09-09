import razorpay
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from user.models import Wallet

KAY_ID = settings.RAZORPAY_KAY_ID
SECRETE_KEY = settings.RAZORPAY_SECRETE_KEY
APP_NAME = settings.RAZORPAY_APP_NAME

rzp_client = razorpay.Client(auth=(KAY_ID, SECRETE_KEY))


@csrf_exempt
def verify_payment(request):
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    rzp_sign = rzp_client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    })
    wallat = Wallet.objects.get(razorpay_order_id=razorpay_order_id)
    wallat.razorpay_payment_id = razorpay_payment_id
    wallat.razorpay_signature = razorpay_signature
    if rzp_sign:
        wallat.status = 'Success'
    else:
        wallat.status = 'Rejected'
    wallat.save()
    return redirect('user_recharge')
