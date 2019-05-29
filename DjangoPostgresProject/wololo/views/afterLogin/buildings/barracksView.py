from django.shortcuts import render, redirect
from django.http import JsonResponse
from wololo.tasks import train_unit
from wololo.helperFunctions import setSumAndLastInteractionDateOfResource, getRequiredTimeForTrainUnits
from wololo.initFirestore import get_db, get_auth
from wololo.firebaseUser import firebaseUser
from wololo.commonFunctions import getGameConfig, getVillageIndex
import urllib.request
import urllib.error

import datetime
import pytz
from celery import chain
import math

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json

db = get_db()
auth = get_auth()
gameConfig = getGameConfig()

@login_required    
def barracks(request, village_index=None):

    user_id = request.user.id
    user = request.user

    if user.is_region_selected is False :
        return redirect("selectRegion")

    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index is 'outOfList'):
        return('barracks')

    my_villages = user.get_my_villages()

    # print (user.myVillages)
    data = { 
        'selectedVillage': my_villages[selected_village_index],
        'gameConfig' : gameConfig,
        'unviewedReportExists' : user.is_unviewed_reports_exists,
        'page' : 'barracks'
    }
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))

    return render(request, 'buildingPages/barracks.html', {'myVillages':my_villages, 'data' : data })


@login_required
def trainUnits(request):
    now = datetime.datetime.now(pytz.utc)
    firing_time = request.POST.get("firingTime") #we should use this instead of now
    user_id = request.user.id
    user = request.user
    selected_village_index = getVillageIndex(request, user, None)  

    village_id = request.POST.get("village_id") 
    unit_type = request.POST.get("unitType") 
    unit_name = request.POST.get("unitName") 
    numberOfUnitsToTrain = int(request.POST.get("value"))


    #if we have resources
    if(user.weHaveResourcesToTrainUnit(village_id, unit_type, unit_name, numberOfUnitsToTrain)):

        village = db.collection('players').document(user_id).collection('villages').document(village_id).get().to_dict()
        reqiured_time = getRequiredTimeForTrainUnits(village, unit_type, unit_name)



        currentWood = user.getCurrentResource(village_id, 'woodCamp')
        currentIron = user.getCurrentResource(village_id, 'ironMine')
        currentClay = user.getCurrentResource(village_id, 'clayPit')

        reqiuredWood = gameConfig['units'][unit_type][unit_name]['Cost']['Wood'] * numberOfUnitsToTrain
        reqiuredIron = gameConfig['units'][unit_type][unit_name]['Cost']['Iron'] * numberOfUnitsToTrain
        reqiuredClay = gameConfig['units'][unit_type][unit_name]['Cost']['Clay'] * numberOfUnitsToTrain

        setSumAndLastInteractionDateOfResource(user_id, village_id, 'woodCamp', currentWood-reqiuredWood, now)
        setSumAndLastInteractionDateOfResource(user_id, village_id, 'clayPit', currentIron-reqiuredIron, now)
        setSumAndLastInteractionDateOfResource(user_id, village_id, 'ironMine', currentClay-reqiuredClay, now)
        # reqiured_time = 10

        result = user.checkTrainingQueueReturnLastOneIfExists(village_id, unit_type)

        if(result == False):
            subtasks = []
            for i in range(numberOfUnitsToTrain):
                subtasks.append(
                    train_unit.si(user_id = user_id, village_id = village_id, unit_type = unit_type, unit_name = unit_name).set(countdown=reqiured_time)
                )
                
            workflow = chain(*subtasks)
            generatedChain = workflow.apply_async()
            chain_id = generatedChain.id
            willEndAt = now + datetime.timedelta(0, reqiured_time*numberOfUnitsToTrain)
            user.addToTrainingQueue(village_id, chain_id, unit_type, unit_name, numberOfUnitsToTrain, now, willEndAt)
        else:
            willStartAt = result['willEndAt']
            print("i will wait in queue totally seconds = >")
            firstTaskDelayedCountdown = math.ceil(((result['willEndAt'] + datetime.timedelta(0, reqiured_time)) - now).total_seconds())
            print(firstTaskDelayedCountdown)

            subtasks = []
            for i in range(numberOfUnitsToTrain):
                if i == 0 :
                    subtasks.append(
                        train_unit.si(user_id = user_id, village_id = village_id, unit_type = unit_type, unit_name = unit_name).set(countdown=firstTaskDelayedCountdown)
                    )
                else:
                    subtasks.append(
                        train_unit.si(user_id = user_id, village_id = village_id, unit_type = unit_type, unit_name = unit_name).set(countdown=reqiured_time)
                    )
                
            workflow = chain(*subtasks)
            generatedChain = workflow.apply_async()
            chain_id = generatedChain.id
            willEndAt = willStartAt + datetime.timedelta(0, reqiured_time*numberOfUnitsToTrain)
            user.addToTrainingQueue(village_id, chain_id, unit_type, unit_name, numberOfUnitsToTrain, willStartAt, willEndAt)
        print(datetime.datetime.now(pytz.utc))
        user.update()
        print(datetime.datetime.now(pytz.utc))
        newResources = user.myVillages[selected_village_index]['buildings']['resources']

        data = {
            'result' : 'Success',
            'newResources' : newResources,
            'newQueueElement' : {
                'willEndAt' : willEndAt,
                'unitName' : unit_name,
                'unitsLeft' : numberOfUnitsToTrain
            }
        }

        return JsonResponse(data)

    else:

        data = {
            "result" : 'Fail'
        }

        return JsonResponse(data)


