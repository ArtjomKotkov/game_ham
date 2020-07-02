from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User

class UserPage(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        context = {
            "target_user":user
        }
        return render(request, 'user_app/user_page.html', context)