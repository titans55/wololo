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
from wololo.models import Villages, get_public_villages
from wololo.helperFunctions import calculate_map_pathfinding

db = get_db()
auth = get_auth()
gameConfig = getGameConfig()

@login_required
def map(request, village_index=None):

    user_id = request.user.id
    user = request.user
    my_villages = user.get_my_villages()

    if user.is_region_selected is False :
        return redirect("selectRegion")
       
    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index is 'outOfList'):
        return redirect('map')

    totalOnMove, totalIncomingStrangerTroops = [], []
    my_villages = user.get_my_villages()
    for village in my_villages:
        for task_id, onMoveElement in village['troops']['onMove'].items():
            onMoveElement['task_id'] = task_id
            totalOnMove.append(onMoveElement)

        for task_id, incomingStrangerTroopsElement in village['troops']['incomingStrangerTroops'].items():
            incomingStrangerTroopsElement['task_id'] = task_id
            totalIncomingStrangerTroops.append(incomingStrangerTroopsElement)

    public_villages = Villages.objects.exclude(user_id=None)
    public_villages_info = get_public_villages(user_id)

    data = { 
        'selectedVillage': my_villages[selected_village_index],
        'gameConfig' : gameConfig,
        'unviewedReportExists' : user.is_unviewed_reports_exists,
        'page' : 'map'
    }
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))

    return render(request, 'map.html', {'publicVillages' : json.dumps(public_villages_info), 'myVillages':my_villages, 'data' : data })

@login_required
def find_path(request):
    if request.method == "POST":
        source_vil_coords = json.loads(request.POST.get("sourceVillageCoords"))
        target_vil_coords = json.loads(request.POST.get("targetVillageCoords"))
        path = calculate_map_pathfinding(source_vil_coords, target_vil_coords)
        data = {
            'path': path
        }
        return JsonResponse(data)