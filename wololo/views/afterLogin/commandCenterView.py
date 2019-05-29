from django.shortcuts import render, redirect
from wololo.firebaseUser import firebaseUser
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.helperFunctions import getVillageInfo, getPublicVillages, getUserIdByVillageId
import json
import datetime
import pytz
from wololo.tasks import attack

gameConfig = getGameConfig()

@login_required    
def commandCenter(request, village_index=None):
    user_id = request.user.id
    user = request.user
    if user.regionSelected is False :
        return redirect("selectRegion")

    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index == 'outOfList'):
        return redirect('commandCenter')

    commandTargetVillageID = request.POST.get("commandTargetVillageID")
    targetVillage = getVillageInfo(commandTargetVillageID)
    print(targetVillage)

    publicVillages = getPublicVillages(user)

    data = { 
        'selectedVillage': user.myVillages[selected_village_index],
        'gameConfig' : gameConfig,
        'targetVillage' : targetVillage,
        'unviewedReportExists' : user.unviewedReportExists,
        'page' : 'commandCenter'
    }
    currentUser = {}
    currentUser['id'] = user_id

    return render(request, 'commandCenter.html', {'currentUser':currentUser, 'publicVillages':json.dumps(publicVillages), 'myVillages':user.myVillages, 'data' : data})

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