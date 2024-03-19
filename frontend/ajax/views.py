from django.http.response import JsonResponse
from ..models import Market
from user.models import CustomUser as User, Wallet



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
        wallet = Wallet.objects.create(
            user = user,
            amount = (avl_amount * 5 / 100), # 5% of available money is reserved
            pay_type = bid,
            status = "Success",
            remark = f"Bid ({bid}) on {market.name}"
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'{e}'})
