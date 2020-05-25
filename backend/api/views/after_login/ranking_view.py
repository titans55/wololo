from django.shortcuts import render, redirect
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.helperFunctions import getAllPlayersOrderedByPoints
from wololo.models import Villages, Users
import json
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt import authentication
from django.contrib.auth.models import User

gameConfig = getGameConfig()


class ranking(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, village_index=None):

        user = request.user
        if user.is_region_selected is False:
            return redirect("selectRegion")

        selected_village_index = getVillageIndex(request, user, village_index)
        if(selected_village_index is 'outOfList'):
            return redirect('ranking')

        allPlayers = getAllPlayersOrderedByPoints()
        print(allPlayers)

        data = {
            'allPlayers': allPlayers,
            'unviewedReportExists': user.is_unviewed_reports_exists,
        }

        return Response(data)

# @login_required
# def ranking(request, village_index=None):
#    user_id = request.user.id
#    user = request.user
#    if user.is_region_selected is False:
#        return redirect("selectRegion")
#
#    selected_village_index = getVillageIndex(request, user, village_index)
#    if(selected_village_index is 'outOfList'):
#        return redirect('ranking')
#
#    allPlayers = getAllPlayersOrderedByPoints()
#    print(allPlayers)
#
#    my_villages = user.get_my_villages()
#
#    data = {
#        'villages_info': my_villages,
#        'selectedVillage': my_villages[selected_village_index],
#        'gameConfig': gameConfig,
#        'allPlayers': allPlayers,
#        'unviewedReportExists': user.is_unviewed_reports_exists,
#        'page': 'ranking'
#    }
#    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
#    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
#
#    return render(request, 'ranking.html', {'myVillages': my_villages, 'data': data})
