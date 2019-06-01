from django.shortcuts import render, redirect
from wololo.firebaseUser import firebaseUser
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.helperFunctions import getAllPlayersOrderedByPoints
from wololo.models import Villages, Users
import json
from django.core.serializers.json import DjangoJSONEncoder

gameConfig = getGameConfig()

@login_required    
def ranking(request, village_index=None):
    user_id = request.user.id
    user = request.user
    if user.is_region_selected is False :
        return redirect("selectRegion")
       
    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index is 'outOfList'):
        return redirect('ranking')

    allPlayers = getAllPlayersOrderedByPoints()
    print(allPlayers)

    my_villages = user.get_my_villages()

    data = { 
        'villages_info' : my_villages,
        'selectedVillage': my_villages[selected_village_index],
        'gameConfig' : gameConfig,
        'allPlayers' : allPlayers,
        'unviewedReportExists' : user.is_unviewed_reports_exists,
        'page' : 'ranking'
    }
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))

    return render(request, 'ranking.html', {'myVillages' : my_villages, 'data' : data})
