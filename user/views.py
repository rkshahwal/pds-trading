from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from permission_decorators import for_admin
from .models import (
    CustomUser as User,
    Wallet,
)
from frontend.models import (
    Banner, Market, MarketBid,
)
from frontend.forms import (
    BannerForm, MarketForm, MarketBidForm,
)

from .forms import (
    UserUpdateForm, WalletForm,
)



@for_admin
def index(request):
    """ Dashboard Page."""
    context = {}
    context["total_user"] = User.objects.count()
    context["total_markets"] = Market.objects.count()
    
    # get total recharged and withdrawal users
    wallet_users = Wallet.objects.select_related().all()
    context["recharge_users"] = wallet_users.filter(
        pay_type='Add Money', status='Success').order_by('user').distinct('user').count()
    context["withdrawal_users"] = wallet_users.filter(
        pay_type='Widrawal', status='Success').order_by('user').distinct('user').count()
    
    context["tot_recharge_amount"] = int(abs(wallet_users.filter(
        pay_type='Add Money', status='Success').aggregate(Sum('amount'))['amount__sum'] or 0))
    context["tot_withdrawal_amount"] = int(abs(wallet_users.filter(
        pay_type='Widrawal', status='Success').aggregate(Sum('amount'))['amount__sum'] or 0))
    
    return render(request, 'user/index.html', context)


def admin_login(request):
    """ Admin Login Method. """
    message = None
    if request.method == "POST":
        mobile = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(mobile_number=mobile, is_staff=True)
        except:
            user = None
        if user:
            if user.check_password(password):
                login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('index')
        message = "Invalid Credentials."
    return render(request, 'user/login.html', {'message': message})


@login_required
def user_logout(request):
    """ Logout method for users"""
    logout(request)
    return redirect('login')


@for_admin
def user_list(request):
    """ All Customers Listing. """
    users = User.objects.filter(is_staff=False)
    rs = request.GET.get('rs', None)
    name = request.GET.get('name', None)
    mobile = request.GET.get('mobile', None)
    salaried = request.GET.get('salaried', None)

    if name:
        users = users.filter(
            Q(name__icontains=name) or
            Q(email__icontains=name))
    
    if mobile:
        users = users.filter(
            mobile_number__icontains=mobile)
    
    if salaried == 'true':
        vip_levels = ['1', '2', '3', '4', '5', '6', '7']
        users = users.filter(
            vip_level__in=vip_levels)
    
    elif salaried == 'false':
        users = users.filter(
            vip_level='0')
    
    if rs:
        if rs == 'recharge':
            wallets = Wallet.objects.filter(
                pay_type="Add Money", status="Success"
            ).order_by('user').distinct('user').values_list('user', flat=True)
            users = users.filter(id__in=wallets)
            
        elif rs == 'withdrawal':
            wallets = Wallet.objects.filter(
                pay_type="Withdrawal", status="Success"
            ).order_by('user').distinct('user').values_list('user', flat=True)
            users = users.filter(id__in=wallets)

    paginator = Paginator(users, 25)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'title': "Users",
        'users': page_obj
    }
    return render(request, 'user/list.html', context)


@for_admin
def user_update(request, id):
    """ Single Customer Update View. """
    user = get_object_or_404(User, id=id)
    form = UserUpdateForm(instance=user)
    if request.method == "POST":
        form = UserUpdateForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated successfully!')
            return redirect('users')
    
    context = {
        'form': form,  
        'title': 'Edit Profile'
    }
    return render(request, 'forms/form.html', context)


@for_admin
def user_delete(request, id):
    """  Delete a single customer from the database."""
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('users')


@for_admin
def user_team(request, id):
    """ referral mlm team a customer. """
    user = get_object_or_404(User, id=id)
    # referal list of user 
    referred_by_user = user.referred_by_me.prefetch_related().all()
    
    # list of users that has refered by user
    referred_by_users = referred_by_user.values('referral_to').distinct()
    users_wallet_list = Wallet.objects.filter(
        user__in=referred_by_users, 
        status="Success").order_by('-created_at')
    recharged_users_list = User.objects.filter(
        id__in = users_wallet_list.values_list('user', flat=True)
    ).distinct()

    referred_by_users_l1 = referred_by_user.filter(
        level = 0, 
        referral_to__in = referred_by_users)
    referred_by_users_l2 = referred_by_user.filter(
        level = 1, 
        referral_to__in = referred_by_users)
    referred_by_users_l3 = referred_by_user.filter(
        level = 2, 
        referral_to__in = referred_by_users)

    recharged_l1 = referred_by_user.filter(
        level = 0, 
        referral_to__in = recharged_users_list)
    recharged_l2 = referred_by_user.filter(
        level = 1, 
        referral_to__in = recharged_users_list)
    recharged_l3 = referred_by_user.filter(
        level = 2,
        referral_to__in = recharged_users_list)
    
    referred_by_users_l1_count = referred_by_users_l1.count()
    referred_by_users_l2_count = referred_by_users_l2.count()
    referred_by_users_l3_count = referred_by_users_l3.count()

    recharged_l1_count = recharged_l1.count()
    recharged_l2_count = recharged_l2.count()
    recharged_l3_count = recharged_l3.count()

    total_recharged_user_count = int(
        recharged_l1_count + recharged_l2_count + recharged_l3_count)
    total_user_count = int(
        referred_by_users_l1_count + referred_by_users_l2_count + referred_by_users_l3_count)
    
    context = {
        'title': f"{user} Team Member's",
        
        'referred_by_users_l1': referred_by_users_l1,
        'referred_by_users_l2': referred_by_users_l2,
        'referred_by_users_l3': referred_by_users_l3,

        'recharged_l1_count': recharged_l1_count,
        'recharged_l2_count': recharged_l2_count,
        'recharged_l3_count': recharged_l3_count,

        'total_recharged_user_count': total_recharged_user_count,
        'total_user_count': total_user_count,
    }
    return render(request, 'user/team.html', context)


"""
Banner Views
"""

@for_admin
def banner_list(request):
    """  Banners listing page. """
    banners = Banner.objects.all()
    context = {
        "title": "Banners",
        "banners": banners
    }
    return  render(request, 'frontend/admin/banner-list.html', context)


@for_admin
def banner_add(request):
    """  Add new banner to the site. """
    form = BannerForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(banner_list)
    else:
        form = BannerForm()
    context = {
        "title": "Add New Banner",
        "form": form
    }
    return render(request, 'forms/form.html', context)



@for_admin
def banner_edit(request, id):
    """ Edit existing banner on the site. """
    banner = get_object_or_404(Banner, id=id)
    form = BannerForm(data=request.POST or None, files=request.FILES or None,  instance=banner)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(banner_list)
    else:
        form = BannerForm(instance=banner)
    context = {
        "title": "Edit Banner",
        "form": form
    }
    return render(request, 'forms/form.html', context)


@for_admin
def banner_delete(request, id):
    """ Delete existing banner on the site. """
    banner = get_object_or_404(Banner, id=id)
    banner.delete()
    return redirect(banner_list)


"""
Wallet Views
"""
@for_admin
def wallet_list(request):
    """  wallets listing page. """
    wallets = Wallet.objects.select_related().all() #.filter(updated_at__gte=timezone.now()-timedelta(weeks=2))
    mobile_number = request.GET.get('mobile', None)
    if mobile_number:
        wallets = wallets.filter(user__mobile_number__icontains=mobile_number)
    pay_type = request.GET.get('pt', None)
    if pay_type:
        wallets = wallets.filter(pay_type__icontains=pay_type)
    pay_method = request.GET.get('pm', None)
    if pay_method:
        wallets = wallets.filter(pay_method__icontains=pay_method)
    utr = request.GET.get('utr', None)
    if utr:
        wallets = wallets.filter(utr__icontains=utr)

    paginator = Paginator(wallets, 100)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "Wallets",
        "wallets": page_obj
    }
    return  render(request, 'wallet/list.html', context)


@for_admin
def wallet_add(request):
    """  Add new Wallet to the site. """
    form = WalletForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(wallet_list)
    else:
        form = WalletForm()
    context = {
        "title": "Add New Wallet",
        "form": form
    }
    return render(request, 'forms/form.html', context)



@for_admin
def wallet_edit(request, id):
    """ Edit existing wallet on the site. """
    wallet = get_object_or_404(wallet, id=id)
    form = WalletForm(data=request.POST or None,  instance=wallet)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(wallet_list)
    else:
        form = WalletForm(instance=wallet)
    context = {
        "title": "Edit wallet",
        "form": form
    }
    return render(request, 'forms/form.html', context)


@for_admin
def wallet_delete(request, id):
    """ Delete existing wallet on the site. """
    wallet = get_object_or_404(Wallet, id=id)
    wallet.delete()
    return redirect(wallet_list)



""" Market Views """
@for_admin
def market_list(request):
    """  markets listing page. """
    markets = Market.objects.all()
    context = {
        "title": "Markets",
        "markets": markets
    }
    return  render(request, 'frontend/admin/market-list.html', context)


@for_admin
def market_add(request):
    """  Add new market to the site. """
    form = MarketForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(market_list)
    else:
        form = MarketForm()
    context = {
        "title": "Add New market",
        "form": form
    }
    return render(request, 'forms/form.html', context)



@for_admin
def market_edit(request, id):
    """ Edit existing market on the site. """
    market = get_object_or_404(Market, id=id)
    form = MarketForm(data=request.POST or None, files=request.FILES or None,  instance=market)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(market_list)
    else:
        form = MarketForm(instance=market)
    context = {
        "title": "Edit market",
        "form": form
    }
    return render(request, 'forms/form.html', context)


@for_admin
def market_delete(request, id):
    """ Delete existing market on the site. """
    market = get_object_or_404(Market, id=id)
    market.delete()
    return redirect(market_list)




"""
 Market Result  Views
"""
@for_admin
def market_bid_list(request):
    """  markets listing page. """
    markets = MarketBid.objects.all()
    context = {
        "title": "Market Bids",
        "markets": markets
    }
    return  render(request, 'market-bid-result/list.html', context)


@for_admin
def market_bid_add(request):
    """  Add new market to the site. """
    form = MarketBidForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(market_bid_list)
    else:
        form = MarketBidForm()
    context = {
        "title": "Add New market",
        "form": form
    }
    return render(request, 'forms/form.html', context)



@for_admin
def market_bid_edit(request, id):
    """ Edit existing market on the site. """
    market = get_object_or_404(MarketBid, id=id)
    form = MarketBidForm(data=request.POST or None,  instance=market)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(market_bid_list)
    else:
        form = MarketBidForm(instance=market)
    context = {
        "title": "Edit market",
        "form": form
    }
    return render(request, 'forms/form.html', context)


@for_admin
def market_bid_delete(request, id):
    """ Delete existing market on the site. """
    market = get_object_or_404(MarketBid, id=id)
    market.delete()
    return redirect(market_bid_list)

