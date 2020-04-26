import os
import json
from django.shortcuts import redirect

def getGameConfig():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'game-config/gameConfig.json')
    with open(file_path, 'r') as f:
        gameConfig = json.load(f)
    return gameConfig

def get_map_data():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'static/wololo/mapAssets/tilemaps/mapv3.json')
    with open(file_path, 'r') as f:
        raw_map_data = json.load(f)
    map_data = {
        'land': raw_map_data['layers'][0]['data'],
        'sea': raw_map_data['layers'][1]['data']
    }
    return map_data

def getVillageIndex(request, user, village_index):
    if village_index is not None and user.number_of_villages>=village_index:
        selected_village_index = int(village_index)
        request.session['selected_village_index'] = selected_village_index
    elif 'selected_village_index' in request.session and user.number_of_villages>request.session['selected_village_index']:
        selected_village_index = request.session['selected_village_index']
    else: 
        selected_village_index = 0
        request.session['selected_village_index'] = 0

    if village_index is not None and user.number_of_villages < village_index:
        request.session['selected_village_index'] = 0
        selected_village_index = 'outOfList'
    
    return selected_village_index


freshVillageBuildingLevels = {
    "townCenter" : 1,
    "woodCamp" : 1,
    "ironMine" : 1,
    "clayPit" : 1, 
    "storage" : 1,
    "farm" : 1,
    "barracks" : 0,
    "stable" : 0,
    "workshop" : 0,
}

def getFreshBuildingLevel(buildingName):

    return freshVillageBuildingLevels[buildingName]

def getFreshVillagePoints():

    return 60
    
def default_fresh_troops_dict():
    return {
        "infantry" :  {
            "Spearman" : 0,
            "Swordsman" : 0,
            "Axeman" : 0,
            "Archer" : 0
        },
        "cavalry" : {
            "Scout" : 0,
            "Light Cavalry": 0,
            "Heavy Cavalry" : 0
        },
        "siegeWeapons" : {
            "Ram" : 0,
            "Catapult": 0
        }
    }

def get_lowest_speed_of_troops(troops):
    units_config = getGameConfig()['units']
    speed_list = []
    for unit_type_name, unit_type in troops.items():
        for unit_name, unit_quantity in unit_type.items():
            speed_list.append(units_config[unit_type_name][unit_name]['speed'])
    return min(speed_list)