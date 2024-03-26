from django.http.response import JsonResponse
from django.db.models import Sum
from ..models import Market, MarketBid
from user.models import CustomUser as User, Wallet
from django.utils import timezone
from datetime import datetime, timedelta



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
            
        # 2 Recharge have done ? or Less amount of recharge
        if not user.wallets.filter(status="Success", pay_type="Add Money").exists():
            return JsonResponse({'success': False, 'error': "Recharge first."})
        
        # 3 If User current total remaining amount < 80% of Recharged Amount 
        user_recharged_amt = user.wallets.filter(
            status="Success", pay_type="Add Money"
        ).aggregate(total=Sum('amount'))['total']
        if (user_recharged_amt / avl_amount)*100 < 80 :
            return JsonResponse({
                    'success':False,
                    'error':'Your Remaining amount is less than 80% of your Recharged amount.'
                })
        
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
                remark = f"Winning ({bid}) on {market.name}"
            )
        else:
            # Loss
            wallet = Wallet.objects.create(
                user = user,
                amount = -(avl_amount * 10 / 100), # 10% of available money is lossed
                pay_type = "Loss",
                status = "Success",
                has_bid = True,
                remark = f"Bid ({bid}) on {market.name}"
            )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'{e}'})
