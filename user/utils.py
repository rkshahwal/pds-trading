from datetime import datetime
import pytz
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
import re


"""phone number validation"""
phone_regex_formate = r"^[6-9]\d{9}$"
phone_invalid_message = "Enter a 10 digit valid mobile number."

# Phone number validator
phone_validator = RegexValidator(
    regex = phone_regex_formate,
    message = phone_invalid_message,
)

name_validator = RegexValidator(
    regex = r"^[A-Z][a-zA-Z '.-]*[A-Za-z][^-]$",
    # message="Enter valid name."
    message="Name must start with capital letter and can contain only letters or spaces."
)

password_regx = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

password_validator = RegexValidator(
    regex = password_regx,
    message = "Use a strong password"
)

def validate_password(password):
    # We use the re.match function to test the password against the pattern
    match = re.match(password_regx, password)
    # return True if the password matches the pattern, False otherwise
    return bool(match)

def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))


def render_index_page(request):
    return redirect('index')

def render_user_home_page(request):
    # Fontend Home page
    return redirect('home')

def page_not_found(request):
    return redirect('home')

def is_weekend():
    today = datetime.now(pytz.timezone(settings.TIME_ZONE))
    return today.weekday() >= 5  # In Python's datetime module, Monday is 0 and Sunday is 6

