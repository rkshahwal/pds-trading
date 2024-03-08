from django.urls import path, include
from .views import *


urlpatterns = [
    # path('ajax/', include('frontend.ajax.urls')),
    path('', index, name='home'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]
