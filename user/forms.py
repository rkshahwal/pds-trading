from typing import Any
from django import forms
from .models import (
    CustomUser as User,
    Wallet,
)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile_number', )
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'mobile_number': forms.NumberInput(attrs={'class': 'form-control', 'readonly':''}),
        }



class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = "__all__"
        
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'pay_type': forms.Select(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'pay_method': forms.TextInput(attrs={'class': 'form-control'}),
            'utr': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }
