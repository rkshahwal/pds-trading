import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from .utils import *
from .managers import CustomUserManager



def generate_unique_6digit_code():
    """
    Generate a random and unique 6-digit number.
    """
    while True:
        code = random.randint(12346, 987987)
        if str(code) not in CustomUser.objects.all().values_list('referral_code', flat=True):
            return code  # Return the unique 6-digit number



class BaseModel(models.Model):
    """abstract base model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)



class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value



class CustomUser(AbstractUser):
    email = LowercaseEmailField()
    mobile_number = models.CharField(
        _("Mobile Number"), max_length=20,
        validators = [phone_validator],
        unique=True
    )
    password = models.CharField(
        _("Password"), max_length=128, validators=[password_validator]
    )
    name = models.CharField(
        _("Full Name"), max_length=100, validators=[name_validator],
        null=True, blank=True
    )
    referral_code = models.CharField(
        _("User Referral Code"),
        max_length=8,
        unique = True,
        null=True, blank=True)
    image = models.ImageField(
        default="default-user.png",
        upload_to="user/image/",
        verbose_name="User Profile Image",
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = ('name', 'email')

    objects = CustomUserManager()

    def __str__(self):
        return str(self.name)+" - "+str(self.mobile_number)
    
    def save(self, *args, **kwargs):
        """ This method is used to modify the password field
        converting text into hashed key"""
        if len(self.password) < 30:
            self.password = make_password(self.password)
        
        if not self.referral_code:
            self.referral_code = generate_unique_6digit_code()

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    @property
    def mobile(self):
        if self.mobile_number:
            return "{}-{}".format(self.mobile_number)
        return ""
    
    @property
    def available_amount(self):
        amt = self.wallets.filter(status="Success").aggregate(total=models.Sum('amount'))['total'] or 0
        return round(amt)

    @property
    def total_revenue(self):
        amt = self.wallets.filter(status="Success", pay_type="Winning").aggregate(total=models.Sum('amount'))['total'] or 0
        return round(amt)
    
    
    @property
    def total_commission(self):
        amt = self.wallets.filter(status="Success", pay_type="Commission").aggregate(total=models.Sum('amount'))['total'] or 0
        return round(amt)




""" Wallet Transactions Model. """
class Wallet(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name = "wallets"
    )
    amount = models.FloatField(
        help_text="Use positive number for Add Money and negative number for Withdrawal"
    )
    pay_type = models.CharField(
        _("Payment Type/Purpose"),
        choices=[
            ("Add Money", "Add Money"), # Positive
            ("Commission", "Commission"), # Positive (Referral Amount)
            ("Bid", "Bid"), # Negative
            ("Winning", "Winning"), # Positive
            ("Loss", "Loss"), # Negative
            ("Widrawal", "Widrawal"), # Negative
        ],
        max_length=20
    )
    status = models.CharField(
        _("Wallet Status"),
        choices=[
            ("Pending", "Pending"),
            ("Success", "Success"),
            ("Hold", "Hold"),
            ("Rejected", "Rejected"),
        ],
        max_length=20,
        default = "Pending"
    )
    pay_method = models.CharField(
        verbose_name="Payment Method",
        max_length=30,
        null=True, blank=True,
        default= " "    # QR or UPI
    )
    utr = models.CharField(
        _("UTR Number"),
        max_length = 100,
        null = True, blank = True
    )
    remark = models.CharField(
        max_length=250,
        null=True, blank=True,
        default= " "
    )
    
    def __str__(self) -> str:
        return str(self.user)+" > "+str(self.amount)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Wallet Transaction")
        verbose_name_plural = _("Wallet Transactions")



class Referral(BaseModel):
    referral_to = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='referral',
        verbose_name = "Referral To", 
        help_text = "User that has created by referrals")
    referred_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='referred_by_me',
        verbose_name = "Referral By")
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.referral_to} referred by {self.referred_by}'
