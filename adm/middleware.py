from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.urls import path


# from libraries.constant import ADMIN_URL, WEB_URL


class RoutePermissions(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        
        # No Permission Required in this urls
        if (
            not request.user.is_authenticated and \
            not request.path.startswith('/login/') and \
            not request.path.startswith('/register/') and \
            not request.path.startswith('/admin/') and \
            not request.path.startswith('/static/') and \
            not request.path.startswith('/media/')):
            return redirect('user_login')

        # Permissions for superuser
        elif (
            (request.user.is_authenticated and request.user.is_superuser) \
            and not request.path.startswith('') and \
            not request.path.startswith('/') and \
            not request.path.startswith('/logout/')) :
                
            raise PermissionDenied
        
        
        # Permissions for Autherised users
        elif (
            (request.user.is_authenticated and request.user.is_active) and \
            not request.path.startswith('') and \
            not request.path.startswith('/logout/')) :
            raise PermissionDenied
        
                    

        # else:
        #     redirect('login_page')
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
