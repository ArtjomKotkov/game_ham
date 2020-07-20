from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import JsonResponse

from .forms import RegisterForm, AuthForm
from combat_app.combat.hero.basic import HEROES_CLASSES
from hero_app.models import Hero
import pprint


class HeroChooseApi(View):

    def get(self, request):
        output = dict(
            items=[hero.serialize() for hero in HEROES_CLASSES.values()]
        )
        return JsonResponse(data=output)


class HeroChooseView(View):

    def get(self, request):
        return render(request, 'main_app/hero_choose.html')

    def post(self, request):
        hero = request.POST.get('hero', None)
        hero_class = request.POST.get('hero_class', None)
        if not hero or not hero_class:
            return JsonResponse(data={}, status=400)
        request.session['hero'] = hero
        request.session['hero_class'] = hero_class
        request.session.save()
        return JsonResponse(data={}, status=200)


class RegisterView(View):

    def get(self, request):
        if not request.session.get('hero', None):
            return redirect(reverse('main_app:hero'))
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'main_app/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects. create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'])
            hero = Hero.create(user=user, hero_name=form.cleaned_data['hero_name'], hero_class=request.session['hero_class'])
            user.heroapp.selected_hero = hero
            del request.session['hero']
            del request.session['hero_class']
            request.session.save()
            user.save()
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
            return redirect(reverse('user:user_page', args=[form.user.username]))
        else:
            context = {
                'form': form
            }
            return render(request, 'main_app/auth.html', context)


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse('main_app:auth'))
