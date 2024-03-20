from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    context = {
        "service": config.SERVICE,
        "group_signal": config.GROUP_SIGNAL_LINK,
        "banners": Banner.objects.all(),
        "markets": Market.objects.filter(status=True),
        "top_markets": Market.objects.filter(status=True).order_by('-latest_price')[:3],
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
            Referral.objects.create(
                referred_by = referred_by,
                referral_to = user
            )
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
    return render(request, 'frontend/mine.html')


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
        "wallets": user.wallets.all()
    }
    return render(request, 'frontend/wallet.html', context)


@login_required
def withdrowal(request):
    context = {
        "tax": config.WITHDRAWAL_FEES_PERCENTAGE
    }
    if request.method == "POST":
        amount = request.POST["amount"]
        wallet = Wallet.objects.create(
            user = request.user,
            amount = -abs(float(amount)),
            status = "Hold",
            pay_type = "Widrawal"
        )
        return redirect('user_wallet')
    return render(request, 'frontend/withdrwal.html', context)


@login_required
def save_bankdetails(request):
    """
    This function is used from the front end to add bank details of a user in his wallete popup.
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
        
    return redirect('user_withdrowal')


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
