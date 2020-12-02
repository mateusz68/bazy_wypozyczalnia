import json
import urllib

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import *


def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'brak_dostepu.html')
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, "login.html", context)


def register_view(request):
    # if request.user.is_authenticated:
    #     return render(request, 'brak_dostepu.html')
    # next = request.GET.get('next')
    # form = UserRegisterForm(request.POST or None)
    # if form.is_valid():
    #     user = form.save(commit=False)
    #     password = form.cleaned_data.get('password1')
    #     email = form.cleaned_data.get("email")
    #     user.set_password(password)
    #     user.save()
    #     new_user = authenticate(email=email, password=password)
    #     login(request, new_user)
    #     if next:
    #         return redirect(next)
    #     return redirect('/')
    # context = {
    #     'form': form,
    # }
    # return render(request, "signup.html", context)
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def register_firma(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = RegisterFormFir(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.czy_firma = True
            user.save()
            new_user = authenticate(email=email, password=raw_password)
            login(request, new_user)
            if next:
                return redirect(next)
            return redirect('wypozyczalnia:index')
    else:
        form = RegisterFormFir()
    return render(request, 'signup.html', {'form': form})


def register_pry(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = RegisterFormPry(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            new_user = authenticate(email=email, password=raw_password)
            login(request, new_user)
            if next:
                return redirect(next)
            return redirect('wypozyczalnia:index')
    else:
        form = RegisterFormPry()
    return render(request, 'signup.html', {'form': form})

