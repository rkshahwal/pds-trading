from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterView, LoginView, ChangePasswordView, user_logout,
    ProfileView, googleAuth, facebookAuth,
    UserVerifyAccountView,
    ForgetPasswordView, ConfirmForgetPasswordView,
    CountryCodeView,
)

router = DefaultRouter()

""" User Register, Login and Profile Urls. """
router.register('country-list', CountryCodeView, basename="country-code-api")
router.register('register', UserRegisterView, basename="user-register-api")
router.register('verify-account-with-otp', UserVerifyAccountView,
                basename="verify-account-with-otp")
router.register('login', LoginView, basename="user-login-api")
router.register('profile', ProfileView, basename="user-profile-api")
router.register('change-password', ChangePasswordView,
                basename="user-change-password-api")
router.register('forget-password', ForgetPasswordView,
                basename="user-forget-password-api")
router.register('confirm-forget-password', ConfirmForgetPasswordView,
                basename="user-confirm-forget-password-api")




urlpatterns = [
    path('', include(router.urls)),
    path('logout/', user_logout, name='user-logout-api'),
    # Social Login
    path('google-auth/', googleAuth),
    path('fb-auth/', facebookAuth),
]
