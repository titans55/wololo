from django.shortcuts import render, redirect
from django.http import JsonResponse
from wololo.initFirestore import get_db, get_auth
from wololo.firebaseUser import firebaseUser
from wololo.commonFunctions import getGameConfig
import urllib.request
import urllib.error
import random
from wololo.models import Villages
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required


db = get_db()
auth = get_auth()
gameConfig = getGameConfig()


@login_required
def selectRegionOnFirstLoginView(request):
    user = request.user
    if user.is_region_selected :
        return redirect('myVillage')

    return render(request, "firstLogin/selectRegion.html")

@login_required
def selectingRegion(request):
    user = request.user
    if user.is_region_selected:
        return redirect('myVillage')
    
    selected_region = request.POST.get("selectedRegion")
    if selected_region != '':
        print(selected_region)
        unowned_villages = Villages.objects.filter(user=None)
        first_village = random.choice(unowned_villages.filter(region__name=selected_region))
        print(first_village.village_name, " selected")
        first_village.user = user
        user.is_region_selected = True
        first_village.save()
        user.save()
    return redirect('myVillage')