from django.shortcuts import render, redirect
from rest_framework.response import Response
from wololo.tasks import train_unit
from wololo.helperFunctions import set_sum_and_last_interaction_date_of_resource
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

from django.db import transaction
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_jwt import authentication
from api.views.after_login.buildings.unit_training_buildings.shared.unit_training_buildings_serializer import UnitsToTrainSerializer
from rest_framework import status

gameConfig = getGameConfig()


class BaseTrainUnitView(APIView):
    unit_type = 'infantry' #OVERRIDE THIS
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        
        serializer = UnitsToTrainSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.datetime.now(pytz.utc)
        user = request.user
        village_id = serializer.initial_data['village_id']
        unit_type = self.unit_type
        vil_obj = Villages.objects.get(id=village_id)

        if user.has_resources_to_train_units(village_id, unit_type, serializer.initial_data['units_to_train']):
            for unit_to_train in serializer.initial_data['units_to_train']:
                number_of_units_to_train = unit_to_train['amount']
                if number_of_units_to_train>0:

                    unit_name = unit_to_train['unit_name']
                    reqiured_time = vil_obj.get_required_time_for_train_units(
                        unit_type, unit_name)

                    current_resources = user.get_current_resources(village_id)

                    reqiuredWood = gameConfig['units'][unit_type][unit_name][
                        'Cost']['Wood'] * number_of_units_to_train
                    reqiuredIron = gameConfig['units'][unit_type][unit_name][
                        'Cost']['Iron'] * number_of_units_to_train
                    reqiuredClay = gameConfig['units'][unit_type][unit_name][
                        'Cost']['Clay'] * number_of_units_to_train

                    # reqiuredWood, reqiuredIron, reqiuredClay = 0, 0, 0  # FOR DEBUGGING
                    reqiured_time = 10  # FOR DEBUGGING

                    set_sum_and_last_interaction_date_of_resource(
                        user.id, village_id, 'woodCamp', current_resources['woodCamp'] - reqiuredWood, now)
                    set_sum_and_last_interaction_date_of_resource(
                        user.id, village_id, 'clayPit', current_resources['ironMine'] - reqiuredIron, now)
                    set_sum_and_last_interaction_date_of_resource(
                        user.id, village_id, 'ironMine', current_resources['clayPit'] - reqiuredClay, now)

                    tq_last_unit_type = vil_obj.get_last_training_queue_by_unit_type(
                        self.unit_type)

                    if(tq_last_unit_type == False):
                        subtasks = []
                        for i in range(number_of_units_to_train):
                            subtasks.append(
                                train_unit.si(user_id=user.id, village_id=village_id, unit_type=unit_type, unit_name=unit_name).set(
                                    countdown=reqiured_time)
                            )

                        workflow = chain(*subtasks)
                        generated_chain = workflow.apply_async()
                        chain_id = generated_chain.id
                        will_end_at = now + \
                            datetime.timedelta(
                                0, reqiured_time * number_of_units_to_train)
                        vil_obj.add_to_training_queue(
                            chain_id, unit_type, unit_name, number_of_units_to_train, now, will_end_at)
                    else:
                        will_start_at = tq_last_unit_type.started_at
                        print("i will wait in queue totally seconds = >")
                        first_task_delayed_countdown = math.ceil(((tq_last_unit_type.will_end_at + datetime.timedelta(0, reqiured_time)) - now).total_seconds())
                        print(first_task_delayed_countdown)

                        subtasks = []
                        for i in range(number_of_units_to_train):
                            if i == 0 :
                                subtasks.append(
                                    train_unit.si(user_id = user.id, village_id = village_id, unit_type = unit_type, unit_name = unit_name).set(countdown=first_task_delayed_countdown)
                                )
                            else:
                                subtasks.append(
                                    train_unit.si(user_id = user.id, village_id = village_id, unit_type = unit_type, unit_name = unit_name).set(countdown=reqiured_time)
                                )
                            
                        workflow = chain(*subtasks)
                        generated_chain = workflow.apply_async()
                        chain_id = generated_chain.id
                        will_end_at = will_start_at + datetime.timedelta(0, reqiured_time*number_of_units_to_train + first_task_delayed_countdown)
                        vil_obj.add_to_training_queue(chain_id, unit_type, unit_name, number_of_units_to_train, will_start_at, will_end_at)

            print(datetime.datetime.now(pytz.utc))
            village_info = user.get_my_village(vil_obj)

            data = {
                'result': 'Success',
                'new_resources': village_info['buildings']['resources'],
                'new_troops': village_info['troops'],
            }

            return Response(data)

        else:
            data = {
                "result": 'Fail',
                "status": "not enough resources"
            }

            return Response(data)
