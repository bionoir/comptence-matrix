from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm


def user_register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f'Your account has been created! You are now able to log in!')
        return redirect('login')
    return render(request, 'users/register.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'users/profile.html')