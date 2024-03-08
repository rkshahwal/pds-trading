from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser as User

from .forms import (
    UserUpdateForm,
)



@login_required(login_url='/user/login/')
def index(request):
    """ Dashbord Page."""
    context = {}
    context["total_user"] = User.objects.count()
    
    return render(request, 'user/index.html', context)


def admin_login(request):
    """ Admin Login Method. """
    message = None
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email, is_staff=True)
        except:
            user = None
        if user:
            if user.check_password(password):
                login(request, user)
                next = request.GET.get('next', None)
                if next:
                    return redirect(next)
                return redirect('index')
        message = "Invalid Credentials."
    return render(request, 'user/login.html', {'message': message})


@login_required
def user_logout(request):
    """ Logout method for users"""
    logout(request)
    return redirect('login')


@login_required
def user_list(request):
    """ All Customers Listing. """
    context = {
        'title': "Users",
        'users': User.objects.filter(is_staff=False)
    }
    return render(request, 'user/list.html', context)


@login_required
def user_update(request, id):
    """ Single Customer Update View. """
    user = get_object_or_404(User, id=id)
    form = UserUpdateForm(instance=user)
    if request.method == "POST":
        form = UserUpdateForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            messages.success(request, f'Profile updated successfully!')
            return redirect('users')
    
    context = {
        'form': form,  
        'title': 'Edit Profile'
    }
    return render(request, 'forms/form.html', context)


@login_required
def user_delete(request, id):
    """  Delete a single customer from the database."""
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('users')
