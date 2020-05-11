from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from wololo.commonFunctions import getGameConfig, getVillageIndex
import urllib.request
import urllib.error
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.decorators import login_required
from wololo.models import Villages, get_public_villages, Users
from wololo.helperFunctions import calculate_map_pathfinding
from rest_framework.views import APIView
from rest_framework.response import Response

gameConfig = getGameConfig()

class MapView(APIView):

    def get(self, request):

        #TODO revert when auth added
        user = Users.objects.get(id=1)
        user_id = user.id

        data = get_public_villages(user.id)

        return Response(data)

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