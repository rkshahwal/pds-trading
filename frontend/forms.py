from django import forms
from .models import (
    Banner, Market, MarketBid,
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



""" Market Bid Form """
class MarketBidForm(forms.ModelForm):
    class Meta:
        model = MarketBid
        fields = "__all__"
        
        widgets = {
            'market': forms.Select(attrs={'class': 'form-control'}),
            'bid': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }
