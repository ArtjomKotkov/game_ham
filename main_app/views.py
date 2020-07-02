from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from .forms import RegisterForm, AuthForm
# Create your views here.

class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'main_app/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])
            login(request, user)
            return redirect('/')
        else:
            context = {
                'form': form
            }
            return render(request, 'main_app/register.html', context)

class AuthView(View):
    def get(self, request):
        form = AuthForm()
        context = {
            'form': form
        }
        return render(request, 'main_app/auth.html', context)

    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/')
        else:
            context = {
                'form': form
            }
            return render(request, 'main_app/auth.html', context)

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse('main_app:auth'))