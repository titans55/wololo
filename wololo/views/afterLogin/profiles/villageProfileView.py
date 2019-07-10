from django.shortcuts import render, redirect
from wololo.firebaseUser import firebaseUser
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from django.core.serializers.json import DjangoJSONEncoder
import json
from wololo.models import Villages

gameConfig = getGameConfig()

@login_required    
def villageProfile(request, village_id, village_index=None):
    user = request.user
    if user.is_region_selected is False :
        return redirect("selectRegion")

    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index == 'outOfList'):
        return redirect('villageProfile')

    try:
        village = Villages.objects.get(id=village_id)
    except:
        #TODO Handle this (village_id doesnt exists)
        return None
    village_info = village.get_village_profile_dict()
    my_villages = user.get_my_villages()

    data = { 
        'selectedVillage': my_villages[selected_village_index],
        'gameConfig' : gameConfig,
        'profileOfVillageInfo' : village_info,
        'unviewedReportExists' : user.is_unviewed_reports_exists,
        'page' : 'villageProfile'
    }
    current_user = {
        'id' : user.id
    }
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
    return render(
        request,
        'profiles/villageProfile.html',
        {
            'currentUser': current_user,
            'myVillages': my_villages,
            'data' : data
        }
    )
