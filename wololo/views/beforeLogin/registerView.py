from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from wololo.forms import RegisterForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if(form.is_valid()):
            print(form.cleaned_data)
            user = form.save()
            login(request, user)

            return redirect(settings.LOGIN_URL)

    form = RegisterForm

    data = {
        'form': form
    }

    return render(request, 'beforeLogin/register.html', data)
