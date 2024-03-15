from django.shortcuts import render, redirect
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
    Banner,
)


@login_required
def home(request):
    context = {
        "service": config.SERVICE,
        "group_signal": config.GROUP_SIGNAL_LINK,
        "banners": Banner.objects.all(),
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
        print(request.POST)
    return render(request, 'frontend/recharge.html')


@login_required
def wallet(request):
    return render(request, 'frontend/wallet.html')


@login_required
def withdrowal(request):
    context = {
        "tax": config.WITHDRAWAL_FEES_PERCENTAGE
    }
    return render(request, 'frontend/withdrwal.html', context)


@login_required
def call_put(request):
    return render(request, 'frontend/call-put.html')


def tc(request):
    tc = """
    Terms and Important Terms:
    All the information given in this website is correct. This is a training game. It is possible to get used to it. I am investing in this website with all my senses,and I have read all its terms and conditions. If in any way I am not affected by this, then  I myself am responsible for the loss, and I am an 18 year old person.
    """
    return HttpResponse(tc)
