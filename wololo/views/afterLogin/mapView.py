from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from wololo.initFirestore import get_db, get_auth
from wololo.firebaseUser import firebaseUser
from wololo.commonFunctions import getGameConfig, getVillageIndex
import urllib.request
import urllib.error
import json

from django.contrib.auth.decorators import login_required
from wololo.models import Villages

db = get_db()
auth = get_auth()
gameConfig = getGameConfig()

@login_required
def map(request, village_index=None):

    user_id = request.user.id
    user = request.user
    my_villages = user.get_my_villages()

    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index == 'outOfList'):
        return redirect('map')

    public_villages = Villages.objects.exclude(user_id=None)
    print(public_villages)
    # publicVillages = public_villages_ref.get()
    publicVillagesInfo = []
    for village in public_villages:
        print(village.user_id_id)
        village._data['village_id'] = village.id
        if(village._data['user_id'] == village.user_id):
            village._data['owner'] = True
            for myVillage in user.myVillages:
                if (village._data['village_id'] == myVillage['id']):
                    myVillage['coords'] = {
                        'x' : village._data['coords']['x'],
                        'y' : village._data['coords']['y']
                    }
        publicVillagesInfo.append(village._data)

    data = { 
        'selectedVillage': my_villages[selected_village_index],
        'gameConfig' : gameConfig,
        'unviewedReportExists' : user.unviewedReportExists,
        'page' : 'map'
    }
    print(data)
    return render(request, 'map.html', {'publicVillages' : json.dumps(publicVillagesInfo), 'myVillages':user.myVillages, 'data' : data })
