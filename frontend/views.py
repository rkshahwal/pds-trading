from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from constance import config
from user.models import (
    CustomUser as User,
    Wallet, Referral,
)
from .models import (
    Banner, Market, UserBankDetail,
)


@login_required
def home(request):
    markets = Market.objects.filter(status=True).order_by('-latest_price')
    context = {
        "service": config.SERVICE,
        "service2": config.SERVICE2,
        "group_signal": config.GROUP_SIGNAL_LINK,
        "banners": Banner.objects.all(),
        "markets": markets,
        "top_markets": markets[:3],
    }
    return render(request, 'frontend/home.html', context)


def user_register(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        code = request.POST.get('code', None)
        
        if code:
            try:    
                referred_by = User.objects.get(
                    referral_code = code
                )
            except Exception as e:
                messages.warning(request, "Invailid Referral Code.")
                return render(request, 'frontend/register.html')
        
        try:    
            user = User.objects.create(
                mobile_number = mobile,
                email = email,
                password = password
            )
        except Exception as e:
            messages.warning(request, f"{e}")
            return render(request, 'frontend/register.html')
        
        if code:
            level = 0
            # First Level Referral
            Referral.objects.create(
                referred_by = referred_by,
                referral_to = user,
                level = 0
            )
            # Wallet.objects.create(
            #     user = referred_by,
            #     amount = 50,
            #     pay_type = "Commission",
            #     remark = "Refer a friend and get Rs.50.",
            # )
            
            # MLM
            while True:
                referrals = Referral.objects.filter(referral_to=referred_by)
                if not referrals.exists():
                    break
                for referral in referrals:
                    referred_by = referral.referred_by
                    Referral.objects.create(
                        referred_by = referred_by,
                        referral_to = user,
                        level = referral.level + 1
                    )
            
        return redirect('user_login')
    return render(request, 'frontend/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        mobile = request.POST.get('username', None)
        password = request.POST.get('password', None)
        try:
            user = User.objects.get(mobile_number=mobile, is_active=True)
        except User.DoesNotExist:
            user = None
            messages.warning(request, "User does not exist")
        if user:
            if user.check_password(password):
                login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('home')
            messages.warning(request, "Invailid Password.")
    return render(request, 'frontend/user-login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def mine(request):
    context = {
        "config": config,
    }
    return render(request, 'frontend/mine.html', context)


@login_required
def recharge(request):
    if request.method == "POST":
        user = request.user
        amount = float(request.POST.get('amount') or 0)
        utr = request.POST.get('utr', None)
        try:
            if amount >= 5000:
                pay_method = "QR"
            else:
                pay_method = "UPI"
            wallet = Wallet.objects.create(
                user = user,
                amount = amount,
                pay_type = "Add Money",
                pay_method = pay_method,
                utr = utr
            )
            return redirect("user_wallet")
        except Exception as e:
            print(e)
    context = {
        "qr": config.QR,
        "upi": config.UPI
    }   
    return render(request, 'frontend/recharge.html', context)


@login_required
def wallet(request):
    user = request.user
    context = {
        "user": user,
        "available": user.available_amount,
        "total_commission": user.total_commission,
        "total_revenue": user.total_revenue,
        "wallets": user.wallets.all()[:100]
    }
    return render(request, 'frontend/wallet.html', context)


@login_required
def withdrowal(request):
    _tax = config.WITHDRAWAL_FEES_PERCENTAGE
    user = request.user
    
    _withdrawalable_amount = user.wallets.filter(
        status="Success",
        pay_type__in = ["Commission", "Bid", "Winning", "Loss", "Widrawal", "Widrawal Charge"]
    ).aggregate(Sum('amount'))['amount__sum'] or 0, # This Amount can be withdra
    
    _recharged_amount = user.wallets.filter(
        status="Success",
        pay_type = "Add Money"
    ).aggregate(Sum('amount'))['amount__sum'] or 0, # Recharged Amont
    
    can_withdrawal = False
    if _withdrawalable_amount[0] >= 300.0: # 300 is winning amount
        can_withdrawal = True
    
    context = {
        "tax": _tax,
        "amount": _withdrawalable_amount[0],
        "can_withdrawal": can_withdrawal        
    }
    
    if request.method == "POST":
        if can_withdrawal:
            amount = abs(float(request.POST["amount"]))
            withdrawal_charge = float(amount) * _tax / 100
            withdrawal_amt = amount - withdrawal_charge
            wallet = Wallet.objects.create(
                user = request.user,
                amount = - withdrawal_amt,
                status = "Hold",
                pay_type = "Widrawal"
            )
            wallet = Wallet.objects.create(
                user = request.user,
                amount = - withdrawal_charge,
                status = "Success",
                pay_type = "Widrawal Charge"
            )
            return redirect('user_wallet')
        else:
            messages.warning(request, "Insufficient balance.")
    return render(request, 'frontend/withdrwal.html', context)


@login_required
def save_bankdetails(request):
    """
    This function is used from the front end to add bank details of a user.
    On his mine > Withdrawal setting option.
    """
    if request.method == "POST":
        name = request.POST.get('account_holder')
        ifsc = request.POST.get('ifsc_code')
        bank_name = request.POST.get('bank_name')
        ac = request.POST.get('account_number')
        
        bank, _created = UserBankDetail.objects.get_or_create(user=request.user)
        bank.name = name
        bank.bank = bank_name
        bank.ifsc = ifsc
        bank.ac = ac
        bank.save()
    return render(request, 'frontend/withdrawal-bank-setting.html')
    # return render(request, 'frontend/bank-details.html')


@login_required
def call_put(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    context = {
        "market": market
    }
    return render(request, 'frontend/call-put.html', context)


def tc(request):
    tc = """
    Terms and Important Terms:
    All the information given in this website is correct. This is a training game. It is possible to get used to it. I am investing in this website with all my senses,and I have read all its terms and conditions. If in any way I am not affected by this, then  I myself am responsible for the loss, and I am an 18 year old person.
    """
    return HttpResponse(tc)


def about_us(request):
    return render(request, "frontend/about-us.html")


def my_team(request):
    referred_by_me = request.user.referred_by_me.prefetch_related('referral_to').all()
    referred_by_me_users = referred_by_me.values('referral_to')
    users_wallet_list = Wallet.objects.filter(user__in=referred_by_me_users).order_by('-created_at')
    users_list = User.objects.filter(
        id__in = users_wallet_list.values_list('user', flat=True)
    )
    context = {
        'l1_list': referred_by_me.filter(level=0),
        'l2_list': referred_by_me.filter(level=1),
        'l3_list': referred_by_me.filter(level=2),
        
        'l1': referred_by_me.filter(level=0, referral_to__in=users_list).distinct().count(),
        'l2': referred_by_me.filter(level=1, referral_to__in=users_list).distinct().count(),
        'l3': referred_by_me.filter(level=2, referral_to__in=users_list).distinct().count(),
    }
    return render(request, "frontend/team.html", context)


@login_required
def password_setting(request):
    # Change Password Views
    
    if request.method == "POST":
        old_password = request.POST.get("old_password", None)
        user = request.user
        
        if not user.check_password(old_password):
            messages.error(request, "Old Password is incorrect.")
            return redirect('password_setting')
        
        else:
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if new_password != confirm_password:
                messages.error(request, "New password and Confirm password are different")
                return redirect('password_setting')
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been changed successfully!")
                return redirect('user_logout')
    return render(request, "frontend/password-setting.html")
