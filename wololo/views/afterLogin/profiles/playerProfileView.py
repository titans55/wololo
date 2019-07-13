from django.shortcuts import render, redirect
from wololo.firebaseUser import firebaseUser
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.models import Users
from django.core.serializers.json import DjangoJSONEncoder
import json

gameConfig = getGameConfig()

@login_required    
def playerProfile(request, player_id, village_index=None):
    user = request.user
    if user.is_region_selected is False :
        return redirect("selectRegion")

    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index == 'outOfList'):
        return redirect('playerProfile')

    try:
        player = Users.objects.get(id=player_id)
    except:
        #TODO Handle this (player_id doesnt exists)
        return None
    player_info = player.get_player_profile_dict()
    my_villages = player.get_my_villages()

    data = { 
        'selectedVillage': my_villages[selected_village_index],
        'gameConfig' : gameConfig,
        'profileOfPlayerID' : player_id,
        'profileOfPlayerInfo' : player_info,
        'unviewedReportExists' : user.is_unviewed_reports_exists,
        'page' : 'playerProfile'
    }
    current_user = {
        'id' : user.id
    }
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
    return render(
        request,
        'profiles/playerProfile.html',
        {
            'currentUser': current_user,
            'myVillages': my_villages,
            'data': data
        }
    )
