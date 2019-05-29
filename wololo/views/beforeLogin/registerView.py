from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse



def registerPage(request):
    
    return render(request, 'beforeLogin/register.html')