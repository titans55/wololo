from django.shortcuts import render, redirect
from django.http import JsonResponse
from wololo.tasks import schedule_upgrade_building
from wololo.helperFunctions import set_sum_and_last_interaction_date_of_resource, getRequiredTimeForUpgrade
from wololo.commonFunctions import getGameConfig, getVillageIndex
import urllib.request
import urllib.error
import json
import datetime
import pytz
from celery import chain
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from wololo.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  permissions
from rest_framework_jwt import authentication
from django.contrib.auth.models import User

gameConfig = getGameConfig()

class VillagesView(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, village_index=None):
        # user_id = request.user.id
        # user = request.user
        #TODO revert when auth added
        user = request.user

        if user.is_region_selected is False :
            return redirect("selectRegion")
        
        selected_village_index = getVillageIndex(request, user, village_index)
        if(selected_village_index is 'outOfList'):
            return redirect('villageApi')

        totalOnMove = []
        totalIncomingStrangerTroops = []

        my_villages = user.get_my_villages()

        for village in my_villages:
            for task_id, onMoveElement in village['troops']['onMove'].items():
                onMoveElement['task_id'] = task_id
                totalOnMove.append(onMoveElement)

            for task_id, incomingStrangerTroopsElement in village['troops']['incomingStrangerTroops'].items():
                incomingStrangerTroopsElement['task_id'] = task_id
                totalIncomingStrangerTroops.append(incomingStrangerTroopsElement)

        print("wololo")
        print(totalOnMove)
        print(totalIncomingStrangerTroops)
        print("wololo")
        my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
        data = { 
            'totalIncomingStrangerTroops' : totalIncomingStrangerTroops,
            'totalOnMove' : totalOnMove,
            'villagesInfo' : my_villages,
            'selectedVillage': my_villages[selected_village_index],
            'gameConfig' : gameConfig,
            'unviewedReportExists' : user.is_unviewed_reports_exists,
            'page' : 'myVillages',
        }

        return Response(data)


# @login_required
# def villages(request, village_index=None):
#     user_id = request.user.id
#     user = request.user

#     if user.is_region_selected is False :
#         return redirect("selectRegion")
       
#     selected_village_index = getVillageIndex(request, user, village_index)
#     if(selected_village_index is 'outOfList'):
#         return redirect('myVillage')

#     totalOnMove = []
#     totalIncomingStrangerTroops = []

#     my_villages = user.get_my_villages()

#     for village in my_villages:
#         for task_id, onMoveElement in village['troops']['onMove'].items():
#             onMoveElement['task_id'] = task_id
#             totalOnMove.append(onMoveElement)

#         for task_id, incomingStrangerTroopsElement in village['troops']['incomingStrangerTroops'].items():
#             incomingStrangerTroopsElement['task_id'] = task_id
#             totalIncomingStrangerTroops.append(incomingStrangerTroopsElement)

#     print("wololo")
#     print(totalOnMove)
#     print(totalIncomingStrangerTroops)
#     print("wololo")

#     data = { 
#         'totalIncomingStrangerTroops' : totalIncomingStrangerTroops,
#         'totalOnMove' : totalOnMove,
#         'villages_info' : my_villages,
#         'selectedVillage': my_villages[selected_village_index],
#         'gameConfig' : gameConfig,
#         'unviewedReportExists' : user.is_unviewed_reports_exists,
#         'page' : 'myVillages'
#     }
#     data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
#     my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
#     print(data['selectedVillage'])
#     return render(request, 'villages.html', {'myVillages':my_villages, 'data' : data})


class UpgradeBuildingView(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, village_index):
        now = datetime.datetime.now(pytz.utc)
        user = request.user
        village_id = request.data.get("village_id")
        print("village_id arrived => ", village_id)
        building_path = request.data.get("building_path")

        # if user.regionSelected is False :
        #     return redirect("selectRegion")

        selected_village_index = getVillageIndex(request, user, village_index)  


        village = user.get_my_villages()[selected_village_index]
        #upgrade_levelTo = village[building_path]['level'] + 1
        if '.' in building_path : 
            # print(village['resources'],"kololo")
            upgrade_levelTo = str(int(village['buildings']['resources'][building_path.split('.')[1]]['level']) + 1)
            required_clay = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['clay']
            required_iron = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['iron']
            required_wood = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['wood']
        else :
            upgrade_levelTo = str(int(village['buildings'][building_path]['level']) + 1)
            required_clay = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['clay']
            required_iron = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['iron']
            required_wood = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['wood']
        #retrieve required resources from gameConfig.json with upgrade_level
        #reqiured_time = getRequiredTimeForUpgrade(village, building_path, upgrade_levelTo)
        reqiured_time = 10
        # required_clay = 0
        # required_iron = 0
        # required_wood = 0
        current_resources = user.get_current_resources(village_id)
        wood_total = current_resources['woodCamp']
        clay_total = current_resources['clayPit']
        iron_total = current_resources['ironMine']

        if(wood_total >= required_wood and iron_total >= required_iron and clay_total >= required_clay):
            with transaction.atomic():
                #update sum and lastInteractionDate of resources (-cost)
                set_sum_and_last_interaction_date_of_resource(user.id, village_id, 'woodCamp', wood_total-required_wood, now)
                set_sum_and_last_interaction_date_of_resource(user.id, village_id, 'clayPit', clay_total-required_clay, now)
                set_sum_and_last_interaction_date_of_resource(user.id, village_id, 'ironMine', iron_total-required_iron, now)
                
                task_id = schedule_upgrade_building.apply_async((user.id, village_id, building_path, upgrade_levelTo), countdown = reqiured_time)
                task_id = task_id.id
                            
                user.set_upgrading_time_and_state(village_id, building_path, reqiured_time, str(task_id), now)

                # print(user.myVillages[selected_village_index]['buildings']['resources'])
                # user.update()
                # newResources = user.myVillages[selected_village_index]['buildings']['resources']

                newResources = user.get_my_villages()[selected_village_index]['buildings']['resources']

                print(newResources)
                data = {
                    'result' : 'Success',
                    'newResources' : newResources
                }
                if( '.' not in building_path):
                    data['newBuilding'] = user.get_my_villages()[selected_village_index]['buildings'][building_path]
                

                print("upgrading")

                print(datetime.datetime.now(pytz.utc))

                return JsonResponse(data)
        else:
            data = {
                'result' : 'Fail',
            }
            print("not enough resources")
            return JsonResponse(data)

# @login_required
# def upgrade(request):
#     if request.method == "POST":
#         print(datetime.datetime.now(pytz.utc))

#         now = datetime.datetime.now(pytz.utc)
#         firing_time = request.POST.get("firingTime") #we should use this instead of now
#         village_id = request.POST.get("village_id")
#         print("village_id arrived => ", village_id)
#         building_path = request.POST.get("building_path")

#         user_id = request.user.id
#         user = request.user
#         # if user.regionSelected is False :
#         #     return redirect("selectRegion")

#         selected_village_index = getVillageIndex(request, user, None)  


#         village = user.get_my_villages()[selected_village_index]
#         #upgrade_levelTo = village[building_path]['level'] + 1
#         if '.' in building_path : 
#             # print(village['resources'],"kololo")
#             upgrade_levelTo = str(int(village['buildings']['resources'][building_path.split('.')[1]]['level']) + 1)
#             required_clay = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['clay']
#             required_iron = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['iron']
#             required_wood = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['wood']
#         else :
#             upgrade_levelTo = str(int(village['buildings'][building_path]['level']) + 1)
#             required_clay = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['clay']
#             required_iron = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['iron']
#             required_wood = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['wood']
#         #retrieve required resources from gameConfig.json with upgrade_level
#         #reqiured_time = getRequiredTimeForUpgrade(village, building_path, upgrade_levelTo)
#         reqiured_time = 10
#         # required_clay = 0
#         # required_iron = 0
#         # required_wood = 0
#         current_resources = user.get_current_resources(village_id)
#         wood_total = current_resources['woodCamp']
#         clay_total = current_resources['clayPit']
#         iron_total = current_resources['ironMine']

#         if(wood_total >= required_wood and iron_total >= required_iron and clay_total >= required_clay):
#             with transaction.atomic():
#                 #update sum and lastInteractionDate of resources (-cost)
#                 set_sum_and_last_interaction_date_of_resource(user_id, village_id, 'woodCamp', wood_total-required_wood, now)
#                 set_sum_and_last_interaction_date_of_resource(user_id, village_id, 'clayPit', clay_total-required_clay, now)
#                 set_sum_and_last_interaction_date_of_resource(user_id, village_id, 'ironMine', iron_total-required_iron, now)
                
#                 task_id = schedule_upgrade_building.apply_async((user_id, village_id, building_path, upgrade_levelTo), countdown = reqiured_time)
#                 task_id = task_id.id
                            
#                 user.set_upgrading_time_and_state(village_id, building_path, reqiured_time, str(task_id), now)

#                 # print(user.myVillages[selected_village_index]['buildings']['resources'])
#                 # user.update()
#                 # newResources = user.myVillages[selected_village_index]['buildings']['resources']

#                 newResources = user.get_my_villages()[selected_village_index]['buildings']['resources']

#                 print(newResources)
#                 data = {
#                     'result' : 'Success',
#                     'newResources' : newResources
#                 }
#                 if( '.' not in building_path):
#                     data['newBuilding'] = user.get_my_villages()[selected_village_index]['buildings'][building_path]
                

#                 print("upgrading")

#                 print(datetime.datetime.now(pytz.utc))

#                 return JsonResponse(data)
#         else:
#             data = {
#                 'result' : 'Fail',
#             }
#             print("not enough resources")
#             return JsonResponse(data)


@login_required
def cancelUpgrade(request):
    now = datetime.datetime.now(pytz.utc)
    village_id = request.POST.get("village_id") 
    building_path = request.POST.get("building_path")
    firing_time = request.POST.get("firingTime")

    user_id = request.user.id
    user = request.user



    user.cancelUpgrading(village_id, building_path, now)

    user.update()
    selected_village_index = getVillageIndex(request, user, None)  
    newResources = user.myVillages[selected_village_index]['buildings']['resources']

    data = {
        'result' : 'Success',
        'newResources' : newResources
    }
    return JsonResponse(data)
