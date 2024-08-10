from django.dispatch import receiver
from django.db.models.signals import post_save
from constance import config
from user.utils import is_weekend
from .models import (
    Wallet
)


def send_bonus(to_user, recharge_amount, level):
    if config.REFERRAL_BONUS_ON:
        """
        Check today id Saturday or Friday in Setting Defined time Zone
        and send the bonus accourding to bellow calculation.
        commission is: 10-15%, 10%, 5% for level upto 3 accordingly.
        """
        recharge_amount = int(recharge_amount)
        bonus_amount = 0

        # Level 1 referal user
        if level == 0:
            if recharge_amount == 500:
                bonus_amount = 50 # 10%
            elif recharge_amount == 1000:
                if is_weekend():
                    bonus_amount = 150 # 15%
                else:
                    bonus_amount = 100 # 10%
        
        # Level 2 referal user
        elif level == 1:
            # 10% of recharged amount
            bonus_amount = recharge_amount * 0.1
        
        # Level 1 referal user
        elif level == 2:
            # 5% of recharged amount
            bonus_amount = recharge_amount * 0.05
        
        if bonus_amount > 0:
            Wallet.objects.create(
                user=to_user,
                status = "Success",
                pay_type = "Bonus",
                amount = float(bonus_amount), # 10% Comision  for Referral User
                remark = f"Bonus earn for on recharge."
            )
    else:
        pass


""" This will send commission or referral user on recharge. """
@receiver(post_save, sender=Wallet)
def wallete_save(sender, instance, created, **kwargs):
    if instance.status == "Success" and instance.pay_type == "Add Money":
        user = instance.user
        user_wallets = user.wallets.filter(status="Success", pay_type="Add Money").count()
        
        # Commission on First Success Recharge
        if not user_wallets > 1:
            # First Level Referral Commission
            try:
                referral_by_0 = user.referral.filter(level=0).first()
                Wallet.objects.create(
                    user = referral_by_0.referred_by,
                    status = "Success",
                    pay_type = "Commission",
                    amount = float(instance.amount * 0.1), # 10% Comision  for Referral User
                    remark = f"Referal user {user.mobile_number} 10% of {instance.amount} recharge commission"
                )
                # Sending Bonus to referred user level 1
                send_bonus(
                    to_user=referral_by_0.referred_by,
                    recharge_amount=instance.amount,
                    level=0
                )
            except Exception as e:
                print(e)
            
            # Sending Bonus to referred user level 2
            try:
                referral_by_1 = user.referral.filter(level=1).first()
                send_bonus(
                    to_user=referral_by_1.referred_by,
                    recharge_amount=instance.amount,
                    level=1
                )
            except Exception as e:
                pass

            # Sending Bonus to referred user level 3
            try:
                referral_by_2 = user.referral.filter(level=2).first()
                send_bonus(
                    to_user=referral_by_2.referred_by,
                    recharge_amount=instance.amount,
                    level=2
                )
            except Exception as e:
                pass
