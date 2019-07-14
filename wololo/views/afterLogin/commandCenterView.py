from django.shortcuts import render, redirect
from wololo.firebaseUser import firebaseUser
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.helperFunctions import getUserIdByVillageId, calculate_map_pathfinding
from wololo.models import Villages, get_public_villages
import json
import datetime
import pytz
from wololo.tasks import attack
from django.core.serializers.json import DjangoJSONEncoder
import json

gameConfig = getGameConfig()

@login_required    
def commandCenter(request, village_index=None):
    user = request.user
    if user.is_region_selected is False :
        return redirect("selectRegion")

    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index == 'outOfList'):
        return redirect('commandCenter')

    target_village_id = request.POST.get("commandTargetVillageID")

    target_village = Villages.objects.get(id=target_village_id)
    target_village_info = target_village.get_village_profile_dict()

    public_villages = get_public_villages(user)
    my_villages = user.get_my_villages()

    source = my_villages[selected_village_index]
    target = target_village_info

    path = calculate_map_pathfinding(source['coords'], target['coords'])

    data = { 
        'selectedVillage': my_villages[selected_village_index],
        'gameConfig': gameConfig,
        'targetVillage': target_village_info,
        'unviewedReportExists': user.is_unviewed_reports_exists,
        'distance': len(path),
        'page': 'commandCenter'
    }
    current_user = {
        'id' : user.id
    }
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
    return render(
        request,
        'commandCenter.html',
        {
            'currentUser': current_user,
            'publicVillages': json.dumps(public_villages),
            'myVillages': my_villages,
            'data': data
        }
    )

def sendAttack(request):
    user_id = request.user.id
    user = request.user
    
    now = datetime.datetime.now(pytz.utc)
    estimatedSeconds = int(request.POST.get("estimatedMinutes"))*60
    attackerTroops = json.loads(request.POST.get("troops")) 
    fromVillageID = request.POST.get("fromVillageID")
    targetVillageID = request.POST.get("targetVillageID")

    estimatedSeconds = 10 #FOR DEBUGGING

    arrivalTime = now + datetime.timedelta(0, estimatedSeconds)

    task_id = attack.apply_async((fromVillageID, targetVillageID, attackerTroops),countdown = estimatedSeconds)
    task_id = task_id.id

    movementDetails = {
        'countdown' : estimatedSeconds,
        'home_village_id' : fromVillageID,
        'target_village_id' : targetVillageID,
        'movementType' : 'attack',
        'state' : 'going',
        'arrivalTime' : arrivalTime
    }
    user.addOnMoveTroops(task_id, movementDetails, attackerTroops)

    defenderUser = firebaseUser(getUserIdByVillageId(targetVillageID))
    defenderUser.addIncomingStrangerTroops(task_id, movementDetails)

    return redirect('myVillage')