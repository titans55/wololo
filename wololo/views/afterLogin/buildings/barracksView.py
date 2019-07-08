from django.shortcuts import render, redirect
from django.http import JsonResponse
from wololo.tasks import train_unit
from wololo.helperFunctions import set_sum_and_last_interaction_date_of_resource
from wololo.initFirestore import get_db, get_auth
from wololo.firebaseUser import firebaseUser
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.models import Villages
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
    selected_village = user.get_my_villages()[selected_village_index] 

    #
    vil_obj = Villages.objects.get(id=selected_village['village_id'])
    print(vil_obj.get_last_training_queue_by_unit_type('infantry'))
    #   

    data = { 
        'selectedVillage': selected_village,
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
    firing_time = request.POST.get("firingTime") #TODO we should use this instead of now
    user_id = request.user.id
    user = request.user
    selected_village_index = getVillageIndex(request, user, None)  
    
    village_id = request.POST.get("village_id") 
    unit_type = request.POST.get("unitType") 
    unit_name = request.POST.get("unitName") 
    number_of_units_to_train = int(request.POST.get("value"))

    vil_obj = Villages.objects.get(id=village_id)

    #if we have resources
    if(user.has_resources_to_train_unit(village_id, unit_type, unit_name, number_of_units_to_train)):

        reqiured_time = vil_obj.get_required_time_for_train_units(unit_type, unit_name)

        current_resources = user.get_current_resources(village_id)

        reqiuredWood = gameConfig['units'][unit_type][unit_name]['Cost']['Wood'] * number_of_units_to_train
        reqiuredIron = gameConfig['units'][unit_type][unit_name]['Cost']['Iron'] * number_of_units_to_train
        reqiuredClay = gameConfig['units'][unit_type][unit_name]['Cost']['Clay'] * number_of_units_to_train

        set_sum_and_last_interaction_date_of_resource(user_id, village_id, 'woodCamp', current_resources['woodCamp']-reqiuredWood, now)
        set_sum_and_last_interaction_date_of_resource(user_id, village_id, 'clayPit', current_resources['ironMine']-reqiuredIron, now)
        set_sum_and_last_interaction_date_of_resource(user_id, village_id, 'ironMine', current_resources['clayPit']-reqiuredClay, now)
        reqiured_time = 10

        # 
        # print(vil_obj.village_troops.in_village_troops_quantity_json)
        #   

        # tq_last_unit_type = user.checkTrainingQueueReturnLastOneIfExists(village_id, unit_type)
        tq_last_unit_type = vil_obj.get_last_training_queue_by_unit_type('infantry')

        if(tq_last_unit_type == False):
            subtasks = []
            for i in range(number_of_units_to_train):
                subtasks.append(
                    train_unit.si(user_id = user_id, village_id = village_id, unit_type = unit_type, unit_name = unit_name).set(countdown=reqiured_time)
                )
                
            workflow = chain(*subtasks)
            generated_chain = workflow.apply_async()
            chain_id = generated_chain.id
            will_end_at = now + datetime.timedelta(0, reqiured_time*number_of_units_to_train)
            vil_obj.add_to_training_queue(chain_id, unit_type, unit_name, number_of_units_to_train, now, will_end_at)
        else:
            will_start_at = tq_last_unit_type.started_at
            print("i will wait in queue totally seconds = >")
            first_task_delayed_countdown = math.ceil(((tq_last_unit_type.will_end_at + datetime.timedelta(0, reqiured_time)) - now).total_seconds())
            print(first_task_delayed_countdown)

            subtasks = []
            for i in range(number_of_units_to_train):
                if i == 0 :
                    subtasks.append(
                        train_unit.si(user_id = user_id, village_id = village_id, unit_type = unit_type, unit_name = unit_name).set(countdown=first_task_delayed_countdown)
                    )
                else:
                    subtasks.append(
                        train_unit.si(user_id = user_id, village_id = village_id, unit_type = unit_type, unit_name = unit_name).set(countdown=reqiured_time)
                    )
                
            workflow = chain(*subtasks)
            generated_chain = workflow.apply_async()
            chain_id = generated_chain.id
            will_end_at = will_start_at + datetime.timedelta(0, reqiured_time*number_of_units_to_train)
            vil_obj.add_to_training_queue(chain_id, unit_type, unit_name, number_of_units_to_train, will_start_at, will_end_at)
        print(datetime.datetime.now(pytz.utc))

        print(datetime.datetime.now(pytz.utc))
        new_resources = user.get_my_villages()[selected_village_index]['buildings']['resources']

        data = {
            'result' : 'Success',
            'newResources' : new_resources,
            'newQueueElement' : {
                'willEndAt' : will_end_at,
                'unitName' : unit_name,
                'unitsLeft' : number_of_units_to_train
            }
        }

        return JsonResponse(data)

    else:

        data = {
            "result" : 'Fail'
        }

        return JsonResponse(data)


