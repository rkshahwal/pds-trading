import hashlib
import requests
from django.http.response import JsonResponse
from django.db.models import Sum
from ..models import Market, MarketBid
from user.models import CustomUser as User, Wallet
from django.utils import timezone
from razor_pay.views import rzp_client, APP_NAME



def call_put_bid(request):
    try:
        m_id = request.POST.get('market_id')
        uid = request.POST.get('uid')
        bid = request.POST.get('bid')
        
        market = Market.objects.get(pk=m_id)
        user = User.objects.prefetch_related('wallets').get(id=uid)
        avl_amount =  user.available_amount
        
        now = timezone.localtime()
        
        # Validations
        # 1 Check if user already make bid for today
        if user.wallets.filter(
            status = "Success",
            has_bid = True,
            created_at__date = now.date()
        ).exists():
            return JsonResponse({
                'success': False,
                'error': "You have already bided today."
            })
        
        # 2 validation chanck if user have permission for bid
        if not user.can_bid:
            return JsonResponse({
                'success': False,
                'error': "You don't have permission to bid."
            })
        
        # 3 Recharge have done ? or Less amount of recharge
        if not user.wallets.filter(status="Success", pay_type="Add Money").exists():
            return JsonResponse({'success': False, 'error': "Recharge first."})
        
        # Process for bid
        # Get Market Bid Result to make make bid for user
        market_bid = MarketBid.objects.filter(
            market=market,
            start_time__lte = now,
            end_time__gte = now,
            bid = bid
        )
        
        if market_bid.exists():
            # Win
            wallet = Wallet.objects.create(
                user = user,
                amount = (avl_amount * 6 / 100), # 6% of available money is winning
                pay_type = "Winning",
                status = "Success",
                has_bid = True,
                market_name = market.name,
                order_option = bid,
                remark = f"Winning ({bid}) on {market.name}"
            )
        else:
            # Loss
            wallet = Wallet.objects.create(
                user = user,
                amount = -(avl_amount * 10 / 100), # 10% of available money is loosed
                pay_type = "Loss",
                status = "Success",
                has_bid = True,
                market_name = market.name,
                order_option = bid,
                remark = f"Bid ({bid}) on {market.name}"
            )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'{e}'})


# Razorpay Recharge
# def recharge(request):
#     if request.method == 'POST':
#         try:
#             data = request.POST
#             user = request.user
#             amount = float(data['amount'])
#             if amount < 100:
#                 return JsonResponse({'success': False, 'error': 'Minimum recharge amount is 100.'})
#             else:
#                 wallet = Wallet.objects.create(
#                     user = user,
#                     amount = amount,
#                     pay_type = "Add Money",
#                     pay_method = "razorpay",
#                 )
                
#                 # Razorpay integrations
#                 DATA = {
#                     "amount": float(amount) * 100,
#                     "currency": "INR",
#                     "receipt": f"{wallet.id}",
#                     "notes": {
#                         "mobile": f"{user.mobile_number}",
#                     }
#                 }
#                 rzp_data = rzp_client.order.create(data=DATA)
#                 wallet.razorpay_order_id = rzp_data['id']
#                 wallet.save()
#                 return JsonResponse({
#                     'success': True,
#                     'app_name': f"{APP_NAME}",
#                     'rzp': rzp_data
#                 })
            
#         except Exception as e:
#             print(e)
#             return JsonResponse({'success': False, 'error': f'{e}'})
        
#     return JsonResponse(405)


# Wepay Recharge
def recharge_wepay(request):
    if request.method == 'POST':
        try:
            data = request.POST
            user = request.user
            amount = float(data['amount'])
            if amount < 100:
                return JsonResponse({'success': False, 'error': 'Minimum recharge amount is 100.'})
            else:
                        
                # Create Wallet
                wallet = Wallet.objects.create(
                    user = user,
                    amount = amount,
                    pay_type = "Add Money",
                    pay_method = "wepay",
                )
                passageId = "17701"
                mchId = "3a614346"
                key= "2b5e7622cfcf42f8877f5e73198120d2"
                callBackUrl = "https://fastwins.pro/payment/verify.php"

                server_name = f'{APP_NAME}'
                # callback_url = 'https://fastwins.pro/trova/src/api/verify.php'
                # notify_url = callback_url
                params = f"amount={amount}&callBackUrl={callBackUrl}&mchId={mchId}&notifyUrl={callBackUrl}&orderNo={wallet.id}&passageId={passageId}&key={key}"

                md5_sign = hashlib.md5(params.encode()).hexdigest()

                payload = {
                    "amount": amount,
                    "callBackUrl": f"{callBackUrl}",
                    "mchId": "3a614346",
                    "notifyUrl": f"{callBackUrl}",
                    "orderNo": wallet.id,
                    "passageId": f"{passageId}",
                    "sign": md5_sign
                }
                response = requests.post('https://apis.wepayplus.com/client/collect/create', json=payload)

                response_data = response.json()

                if response_data.get('success') and 'payUrl' in response_data['data']:
                    sql1 = "INSERT INTO recharge (username, recharge, status, upi, utr, rand) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (user, amount, 'unpaid', '0', '0', wallet.id)

                    print(f"Location: {response_data['data']}")

                return JsonResponse({
                    'success': True,
                    'app_name': f"{APP_NAME}",
                    'wepay': response['data']
                })
            
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': f'{e}'})
        
    return JsonResponse(405)
