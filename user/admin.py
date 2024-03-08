from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'mobile_number', 'referral_code',
        'date_joined', 'is_active'
    )
    readonly_fields = ("referral_code",)
    list_editable = ('is_active',)
    list_filter = ('date_joined', 'is_active')
    search_fields = ('name', 'email', 'mobile_number')
    
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
    list_display = ('user', 'amount', 'status', 'pay_method', 'utr', 'created_at')
    search_fields = ('user__name', 'user__email', 'utr')
    list_filter = ('status', 'created_at')


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referral_to', 'referred_by', 'level')
    list_filter = ('level', )
