from typing import Any
from django import forms
from .models import CustomUser as User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile_number', )
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'mobile_number': forms.NumberInput(attrs={'class': 'form-control', 'readonly':''}),
        }
