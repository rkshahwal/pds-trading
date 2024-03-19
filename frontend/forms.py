from django import forms
from .models import (
    Banner, Market,
)



class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"
        
        widgets = {
            'alt': forms.TextInput(attrs={'class': 'form-control'}),
        }




""" Market Form """
class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = "__all__"
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'latest_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'fun_range': forms.NumberInput(attrs={'class': 'form-control'}),
        }
