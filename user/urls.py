from django.urls import path, include
from .views import *


urlpatterns = [
    path('ajax/', include('user.ajax.urls')),
    path('', index, name='index'),
    path('login/', admin_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('users/', user_list, name='users'),
    path('edit-user/<int:id>/', user_update, name='edit-user'),
    path('delete-user/<int:id>/', user_delete, name='delete-user'),
    path('user-teams/<int:id>/', user_team, name='user-team'),
    
    # Banner Urls
    path('banners/', banner_list, name='banners'),
    path('add-banner/', banner_add, name='add-banner'),
    path('edit-banner/<int:id>/', banner_edit, name='edit-banner'),
    path('delete-banner/<int:id>/', banner_delete, name='delete-banner'),
    
    # Market Urls
    path('markets/', market_list, name='markets'),
    path('add-market/', market_add, name='add-market'),
    path('edit-market/<int:id>/', market_edit, name='edit-market'),
    path('delete-market/<int:id>/', market_delete, name='delete-market'),
    
    
    # Wallet Urls
    path('wallets/', wallet_list, name='wallets'),
    path('add-wallet/', wallet_add, name='add-wallet'),
    path('edit-wallet/<int:id>/', wallet_edit, name='edit-wallet'),
    path('delete-wallet/<int:id>/', wallet_delete, name='delete-wallet'),
    
    
    # Market Result Url
    path('market-bids/', market_bid_list, name='market-bids'),
    path('add-market-bid/', market_bid_add, name='add-market-bid'),
    path('edit-market-bid/<int:id>/', market_bid_edit, name='edit-market-bid'),
    path('delete-market-bid/<int:id>/', market_bid_delete, name='delete-market-bid'),
]
