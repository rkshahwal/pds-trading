from django.urls import path, include
from .views import *


urlpatterns = [
    # path('api/', include('user.api.urls')),
    path('ajax/', include('user.ajax.urls')),
    path('', index, name='index'),
    path('login/', admin_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('users/', user_list, name='users'),
    path('edit-user/<int:id>/', user_update, name='edit-user'),
    path('delete-user/<int:id>/', user_delete, name='delete-user'),
    
    path('banners/', banner_list, name='banners'),
    path('add-banner/', banner_add, name='add-banner'),
    path('edit-banner/<int:id>/', banner_edit, name='edit-banner'),
    path('delete-banner/<int:id>/', banner_delete, name='delete-banner'),
]
