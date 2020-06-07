from django.shortcuts import render, redirect
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex, get_lowest_speed_of_troops
from wololo.helperFunctions import getUserIdByVillageId, calculate_map_pathfinding
from wololo.models import Villages, get_public_villages, TroopMovements
import datetime
import pytz
from wololo.tasks import attack
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from api.views.after_login.command_center.serializers.source_target_village_serializer import SourceTargetVillageIdsSerializer
from rest_framework import permissions
from rest_framework_jwt import authentication
from .serializers.source_target_village_serializer import SourceTargetVillageIdsSerializer
from rest_framework import status

gameConfig = getGameConfig()


class CalculateDistanceBetweenTwoVillages(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = SourceTargetVillageIdsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        source_village = Villages.objects.get(
            id=serializer.initial_data['source_village_id'])

        target_village = Villages.objects.get(
            id=serializer.initial_data['target_village_id'])

        path = calculate_map_pathfinding(
            source_village.get_coords_dict(), target_village.get_coords_dict()
        )

        data = {
            'sourceVillage': source_village.get_village_profile_dict(),
            'targetVillage': target_village.get_village_profile_dict(),
            'path': path,
            'distance': len(path),
        }

        return Response(
            data
        )


class AttackView(APIView):
    # authentication_classes = (authentication.JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request, village_id):
        user = request.user

        # if source_village.user != user:
        #     raise Exception("you are not owner of source village")

        now = datetime.datetime.now(pytz.utc)
        attacker_troops = json.loads(request.POST.get("troops"))
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

        tile_per_min_speed = get_lowest_speed_of_troops(attacker_troops)
        movement_duration_seconds = (len(path) / (tile_per_min_speed)) * 60
        movement_duration_seconds = 10  # FOR DEBUGGING

        arrival_time = now + datetime.timedelta(0, movement_duration_seconds)

        for unitTypeName, unitType in attacker_troops.items():
            for unitName, unit_quantity in unitType.items():
                from_village.village_troops.in_village_troops_quantity_json\
                    [unitTypeName][unitName] -= unit_quantity
                from_village.village_troops.on_move_troops_quantity_json\
                    [unitTypeName][unitName] += unit_quantity

        from_village.village_troops.save()

        task_id = attack.apply_async(
            (fromVillageID, targetVillageID, attacker_troops), countdown=movement_duration_seconds)
        task_id = task_id.id

        TroopMovements.objects.create(
            task_id=task_id,
            arrival_time=arrival_time,
            movement_duration_seconds=movement_duration_seconds,
            movement_type='attack',
            state='going',
            moving_troops_json=attacker_troops,
            home_village=from_village,
            target_village=target_village
        )
        # TODO remove inVIllage troops add to onMove troops
        # user.addOnMoveTroops(task_id, movementDetails, attacker_troops)

        # defenderUser = firebaseUser(getUserIdByVillageId(targetVillageID))
        # defenderUser.addIncomingStrangerTroops(task_id, movementDetails)

        pass


def sendAttack(request):
    user_id = request.user.id
    user = request.user

    with transaction.atomic():

        now = datetime.datetime.now(pytz.utc)
        attacker_troops = json.loads(request.POST.get("troops"))
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

        tile_per_min_speed = get_lowest_speed_of_troops(attacker_troops)
        movement_duration_seconds = (len(path) / (tile_per_min_speed)) * 60
        movement_duration_seconds = 10  # FOR DEBUGGING

        arrival_time = now + datetime.timedelta(0, movement_duration_seconds)

        for unitTypeName, unitType in attacker_troops.items():
            for unitName, unit_quantity in unitType.items():
                from_village.village_troops.in_village_troops_quantity_json\
                    [unitTypeName][unitName] -= unit_quantity
                from_village.village_troops.on_move_troops_quantity_json\
                    [unitTypeName][unitName] += unit_quantity

        from_village.village_troops.save()

        task_id = attack.apply_async(
            (fromVillageID, targetVillageID, attacker_troops), countdown=movement_duration_seconds)
        task_id = task_id.id

        TroopMovements.objects.create(
            task_id=task_id,
            arrival_time=arrival_time,
            movement_duration_seconds=movement_duration_seconds,
            movement_type='attack',
            state='going',
            moving_troops_json=attacker_troops,
            home_village=from_village,
            target_village=target_village
        )
        # TODO remove inVIllage troops add to onMove troops
        # user.addOnMoveTroops(task_id, movementDetails, attacker_troops)

        # defenderUser = firebaseUser(getUserIdByVillageId(targetVillageID))
        # defenderUser.addIncomingStrangerTroops(task_id, movementDetails)

    return redirect('myVillage')
