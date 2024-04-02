from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import (
    Wallet
)


""" This will send commission or referral user on recharge. """
@receiver(post_save, sender=Wallet)
def wallete_save(sender, instance, created, **kwargs):
    if instance.status == "Success" and instance.pay_type == "Add Money":
        user = instance.user
        if not user.wallets.filter(status="Success", pay_type="Add Money").exists():
            # Level First Commission
            try:
                referral_by_0 = user.referral.filter(level=0).first()
                Wallet.objects.create(
                    user = referral_by_0.referred_by,
                    status = "Success",
                    pay_type = "Commission",
                    amount = float(instance.amount * 0.1), # 10% Comision  for Referral User
                    remark = f"Referal user {user.mobile_number} 10% of {instance.amount} recharge commission"
                )
            except Exception as e:
                print(e)
