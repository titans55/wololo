from django.shortcuts import render, redirect
from wololo.firebaseUser import firebaseUser
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex, get_lowest_speed_of_troops
from wololo.helperFunctions import getUserIdByVillageId, calculate_map_pathfinding
from wololo.models import Villages, get_public_villages, TroopMovements
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

    #TODO improve this code
    target_village_id = request.POST.get("commandTargetVillageID")

    target_village = Villages.objects.get(id=target_village_id)
    target_village_info = target_village.get_village_profile_dict()

    my_villages = user.get_my_villages()

    source = my_villages[selected_village_index]
    target = target_village_info
    # DRY !!!

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
    public_villages = get_public_villages(user)

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
    attackerTroops = json.loads(request.POST.get("troops")) 
    fromVillageID = int(request.POST.get("fromVillageID"))
    targetVillageID = int(request.POST.get("targetVillageID"))

    from_village = Villages.objects.get(id=fromVillageID)
    target_village = Villages.objects.get(id=targetVillageID)


    path = calculate_map_pathfinding(
        {
            'x': from_village.coords_x,
            'y': from_village.coords_y,
        }, 
        {
            'x': target_village.coords_x,
            'y': target_village.coords_y,
        }
    )
    
    tile_per_min_speed = get_lowest_speed_of_troops(attackerTroops)
    movement_duration_seconds = (len(path)/(tile_per_min_speed))*60 
    movement_duration_seconds = 10 #FOR DEBUGGING

    arrival_time = now + datetime.timedelta(0, movement_duration_seconds)

    task_id = attack.apply_async((fromVillageID, targetVillageID, attackerTroops),countdown = movement_duration_seconds)
    task_id = task_id.id

    TroopMovements.objects.create(
        task_id=task_id,
        arrival_time=arrival_time,
        movement_duration_seconds=movement_duration_seconds,
        movement_type='attack',
        state='going',
        moving_troops_json=attackerTroops,
        home_village=Villages.objects.get(id=fromVillageID),
        target_village=Villages.objects.get(id=targetVillageID)
    )
    #TODO remove inVIllage troops add to onMove troops
    # user.addOnMoveTroops(task_id, movementDetails, attackerTroops)

    # defenderUser = firebaseUser(getUserIdByVillageId(targetVillageID))
    # defenderUser.addIncomingStrangerTroops(task_id, movementDetails)

    return redirect('myVillage')