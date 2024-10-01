from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from user.models import Wallet


@csrf_exempt
def verify_payment_wepay(request):
    orderNo = request.GET.get('orderNo')
    amount = request.GET.get('amount')
    # payStatus	Payment status, 0-order generated, 1-payment successful, 2-payment failed
    payStatus = request.GET.get('payStatus') 
    remark = request.GET.get('remark', '')
    sign = request.GET.get('sign', '')

    print(f"orderNo:{orderNo}, amount: {amount}, payStatus:{payStatus}, remark: {remark}, sign: {sign}")

    wallat = Wallet.objects.get(id=int(orderNo))
    try:
        if payStatus == 1:
            wallat.status = "Success"
        
        elif payStatus == 2:
            wallat.status = 'Rejected'
        wallat.remark = remark
    
    except:
        wallat.status = 'Rejected'
    
    wallat.save()
    return redirect('user_recharge')


@csrf_exempt
def notify_payment_wepay(request):
    orderNo = request.GET.get('orderNo')
    amount = request.GET.get('amount')
    # payStatus	Payment status, 0-order generated, 1-payment successful, 2-payment failed
    payStatus = request.GET.get('payStatus') 
    remark = request.GET.get('remark', '')
    sign = request.GET.get('sign', '')

    print(f"orderNo:{orderNo}, amount: {amount}, payStatus:{payStatus}, remark: {remark}, sign: {sign}")

    wallat = Wallet.objects.get(id=int(orderNo))
    try:
        if payStatus == 1:
            wallat.status = "Success"
        
        elif payStatus == 2:
            wallat.status = 'Rejected'
        wallat.remark = remark
    
    except:
        wallat.status = 'Rejected'
    
    wallat.save()
    
