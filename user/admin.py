from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'mobile_number', 'referral_code', 'can_bid',
        'date_joined', 'is_active', 'vip_level',
    )
    readonly_fields = ("referral_code",)
    list_editable = ('is_active', 'can_bid',)
    list_filter = ('date_joined', 'is_active', 'can_bid', 'vip_level')
    search_fields = ('name', 'email', 'mobile_number', 'referral_code')
    
    fieldsets = (
        ("Profile", {
            "classes": ("wide",),  # A custom CSS class that will be applied to the fieldset.
            "fields": ("name", "email", "mobile_number", "referral_code", "image")
        }),
        ("Password and Authorization", {
            "classes": ("collapse",),  # A custom CSS class that will be applied to the fieldset, and makes it collaps
            "fields": ("password",),
        }),
        ("More options", {
            "classes": ("collapse",),
            "fields": (
                "is_active", "is_staff", "is_superuser",
            )
        })
    )
    

@admin.register(Wallet)
class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'pay_type', 'pay_method', 'utr', 'market_name', 'has_bid', 'created_at',)
    search_fields = ('user__name', 'user__email', 'user__mobile_number', 'utr')
    list_editable = ("pay_type", "pay_method", "status",)
    list_filter = ('status', 'has_bid', 'pay_type', 'market_name', 'created_at')


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referral_to', 'referred_by', 'level')
    list_filter = ('level', )
    search_fields = ('referral_to__mobile_number', 'referred_by__mobile_number',)
    list_editable = ('level', )
