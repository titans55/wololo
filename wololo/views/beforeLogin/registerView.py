from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from wololo.forms import RegisterForm
from django.contrib.auth import login
from django.views import View


class RegisterView(View):

    def get(self, request, *args, **kwargs):

        form = RegisterForm()
        data = {
            'form': form
        }

        return render(request, 'beforeLogin/register.html', data)

    def post(self, request, *args, **kwargs):

        form = RegisterForm(request.POST)
        if(form.is_valid()):
            print(form.cleaned_data)
            user = form.save()
            login(request, user)

            return redirect(settings.LOGIN_URL)
