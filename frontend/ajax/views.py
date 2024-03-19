from django.http.response import JsonResponse
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
        user = User.objects.get(id=uid)
        avl_amount =  user.available_amount
        
        if avl_amount < 500:
            return JsonResponse({'success': False, 'error': "Less available amount."})
        
        now = timezone.localtime()
        print(now)
        
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
                amount = (avl_amount * 6 / 100), # 5% of available money is winning
                pay_type = "Winning",
                status = "Success",
                remark = f"Winning ({bid}) on {market.name}"
            )
        else:
            # Loss
            wallet = Wallet.objects.create(
                user = user,
                amount = -(avl_amount * 10 / 100), # 10% of available money is lossed
                pay_type = "Loss",
                status = "Success",
                remark = f"Bid ({bid}) on {market.name}"
            )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'{e}'})
