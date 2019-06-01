from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from wololo.initFirestore import get_db, get_auth
from wololo.firebaseUser import firebaseUser
from wololo.commonFunctions import getGameConfig, getVillageIndex
import urllib.request
import urllib.error
import json
from django.core.serializers.json import DjangoJSONEncoder

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

    my_villages = user.get_my_villages()
    for village in my_villages:
        for task_id, onMoveElement in village['troops']['onMove'].items():
            onMoveElement['task_id'] = task_id
            totalOnMove.append(onMoveElement)

        for task_id, incomingStrangerTroopsElement in village['troops']['incomingStrangerTroops'].items():
            incomingStrangerTroopsElement['task_id'] = task_id
            totalIncomingStrangerTroops.append(incomingStrangerTroopsElement)

    public_villages = Villages.objects.exclude(user_id=None)
    print(public_villages)
    # publicVillages = public_villages_ref.get()
    publicVillagesInfo = []

    for village in public_villages:
        village_dict = {}
        village_dict['user_id'] = village.user_id
        village_dict['village_id'] = village.id
        if(village_dict['user_id'] == user_id):
            village_dict['owner'] = True
        village_dict['coords'] = {
            'x' : village.coords_x,
            'y' : village.coords_y
        }
        village_dict['villageName'] = village.village_name
        village_dict['playerName'] = str(village.user)
        village_dict['points'] = village.points
        print(village_dict)
            # for myVillage in user.myVillages:
            #     if (village_dict['village_id'] == myVillage['id']):
            #         myVillage['coords'] = {
            #             'x' : village_dict['coords']['x'],
            #             'y' : village_dict['coords']['y']
            #         }
        publicVillagesInfo.append(village_dict)

    data = { 
        'selectedVillage': my_villages[selected_village_index],
        'gameConfig' : gameConfig,
        'unviewedReportExists' : user.is_unviewed_reports_exists,
        'page' : 'map'
    }
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
    print(publicVillagesInfo)
    return render(request, 'map.html', {'publicVillages' : json.dumps(publicVillagesInfo), 'myVillages':my_villages, 'data' : data })
