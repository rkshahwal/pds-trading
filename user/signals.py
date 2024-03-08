from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from random import randint
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from .models import (
    CustomUser as User,
)


""" This will create send otp on his mail. """
@receiver(post_save, sender=User)
def user_creation(sender, instance, created, **kwargs):
    if created:
        pass
        # Sending otp on his mail
        # otp = randint(100000, 999999)
        # instance.otp = otp
        # instance.last_login = timezone.datetime.now()
        # instance.save()
        # email_context = {
        #     "message": f"Hii, {instance.name} please verify your account with entering otp: {otp}",
        #     "name": "Astro Stone",
        #     "email": f"{settings.DEFAULT_FROM_EMAIL}"
        # }
        # email_message = render_to_string(
        #     'user/email/created.html', email_context
        # )
        # email = EmailMessage(
        #     subject = "Chess Champion: Account Email Confirmation",
        #     body = email_message,
        #     to = [instance.email]
        # )
        # email.send(fail_silently=False)
        
