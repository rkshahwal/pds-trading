"""
URL configuration for adm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from user.utils import page_not_found
from .constance_config_view import update_confi_setting
from frontend.cronjob import send_salary

admin.site.site_header = "ADM Treding Administration"
admin.site.site_title = "ADM"

urlpatterns = [
    path('', include('frontend.urls')),
    path('admin/setting/', update_confi_setting, name="update-setting"),
    path('admin/', include('user.urls')),
    path('super-admin/', admin.site.urls),
    path('send-salary/', send_salary),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^.*$', page_not_found, name="page_not_found"),]
