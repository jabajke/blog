from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .forms import SignUpForm, LoginForm


def signup(request):
    form = SignUpForm(request.POST or None)
    error = ''
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd['username'],
                is_active=True,
            )
            user.set_password(cd['password1'])
            user.save()

            return redirect('success')
        error += 'User with such email already exists'

    return render(request, template_name='authapp/signup.html', context={
        'form': form,
        'title': 'Signup',
        'error': error
    })


def login_view(request):
    form = LoginForm(request.POST or None)
    error = ''
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('success')
            error += 'Username or password are incorrect'
    return render(request, 'authapp/login.html', context={
        'form': form,
        'error': error
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
