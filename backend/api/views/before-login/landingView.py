from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


def landingPage(request):
    if('loggedIn' in request.session):
        if (request.session['loggedIn']):
            return redirect('myVillage')

    return render(request, 'beforeLogin/landingPage.html')