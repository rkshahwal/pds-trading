from django.http.response import JsonResponse
from ..models import CustomUser as User, Wallet



def update_user_active(request):
    # Update user bid status
    user_id = request.POST.get('user_id')
    new_status = int(request.POST.get('new_status'))
    try:
        user = User.objects.get(pk=user_id)
        user.can_bid = bool(new_status)
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})


def update_wallet_status(request):
    w_id = request.POST.get('wallet_id')
    new_status = request.POST.get('new_status')
    try:
        wallet = Wallet.objects.get(pk=w_id)
        wallet.status = new_status
        wallet.save()
        return JsonResponse({'success': True})
    except Wallet.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Wallet not found'})
