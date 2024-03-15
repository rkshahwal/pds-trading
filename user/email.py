from django.conf import settings as setting_project
from django.contrib.auth.tokens import default_token_generator
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from .models import CustomUser
from .utils import encode_uid, decode_uid



""" Reset Password Link Send to User Email. """
def password_reset(request):
    if request.method == "POST":
        email=request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
        except:
            user = None
        if user:
            uid = encode_uid(user.pk)
            token = default_token_generator.make_token(user)
            reset_link = f"{request.META['HTTP_ORIGIN']}/set-password/{uid}/{token}/"
            context = {
                'user': user,
                'reset_link': reset_link,
            }
            email = send_mail(
                subject = "ADM - Password Reset",
                message = render_to_string('user/email/password-reset.html', context),
                recipient_list = [user.email,],
                fail_silently = False,
                from_email = setting_project.DEFAULT_FROM_EMAIL
            )
            return HttpResponse("Reset Password link sent successfully. \nCheck Your email and set the password.")
    return render(request, "password/send-reset-link.html")



""" Set User password . """
def password_reset_confirm(request, uid, token):
    user = get_object_or_404(CustomUser, pk=decode_uid(uid))
    if user:
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                password = request.POST['password']
                user.set_password(password)
                user.save()
                return redirect("user_login")
        else:
            return HttpResponse("Link has expired. Try again.")
    return render(request, "password/password-set.html")
