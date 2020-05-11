import datetime
import json
import os
import dateutil.parser
import pytz
from .commonFunctions import getGameConfig, get_map_data
import datetime
import math
from wololo.models import Users, VillageBuildings, ResourceBuildingDetails, VillageBuildings, Villages
import numpy as np


gameConfig = getGameConfig()





def set_sum_and_last_interaction_date_of_resource(user_id, village_id, resourceBuilding, newSum, now):

    resource_building = VillageBuildings.objects.get(village_id = village_id, building_name = resourceBuilding)
    rbd = ResourceBuildingDetails.objects.get(id = str(resource_building.resource_building_detail_id))
    rbd.sum = newSum
    rbd.last_interaction_date = now
    rbd.save()
    # village = db.collection('players').document(user_id).collection('villages').document(village_id)
    # village.update({
    #     'buildings.resources.'+resourceBuilding+'.sum' : newSum,
    #     'buildings.resources.'+resourceBuilding+'.lastInteractionDate' : now,
    # })

    return True

def getRequiredTimeForUpgrade(village, building_path, upgrade_levelTo):
    
    if '.' in building_path :
        reqiured_time = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradeTime'][upgrade_levelTo] 
    else:
        reqiured_time = gameConfig['buildings'][building_path]['upgradeTime'][upgrade_levelTo]

    speedPercantageOfTownCenter = gameConfig['buildings']['townCenter']['buildingSpeed'][str(village['buildings']['townCenter']['level'])]
    reqiured_time = int(reqiured_time - (reqiured_time * speedPercantageOfTownCenter / 100 )) * 60 #seconds
    
    return reqiured_time

def calculate_points_for_village(village_id):

    village_buildings = VillageBuildings.objects.filter(village_id=village_id)
    calculated_points = 0

    for vb in village_buildings:
        if vb.is_resource_building:
            point_of_building = gameConfig['buildings']['resources'][vb.building_name]['pointByLevel'][str(vb.level)]
            calculated_points += point_of_building
        else:
            point_of_building = gameConfig['buildings'][vb.building_name]['pointByLevel'][str(vb.level)]
            calculated_points += point_of_building
    vil = Villages.objects.get(id=village_id)
    vil.points = calculated_points
    vil.save()
    calculate_points_for_player(vil.user.id)

def calculate_points_for_player(user_id):
  
    player = Users.objects.get(id=user_id)
    players_villages = Villages.objects.filter(user=player)
    calculated_points = 0
    
    for village in players_villages: 
        village_points = village.points   
        calculated_points += village_points
    player.points = calculated_points
    player.save()
    
def getAllPlayersOrderedByPoints():

    users = Users.objects.all().filter(number_of_villages__gte = 0)
    print(users)
    players = []
    for player in users: 
        player_dict = {}
        player_dict['username'] = str(player)
        player_dict['numberOfVillages'] = player.number_of_villages
        player_dict['id'] = player.id
        player_dict['points'] = player.points
        players.append(player_dict)


    players = sorted(players, key = lambda i: i['points'], reverse=True) 

    return players

def getUserIdByVillageId(village_id):
    public_villages_ref = db.collection('villages')
    return public_villages_ref.document(village_id).get({'user_id'}).to_dict()['user_id']

def createEmptyDictionaryForBattleReport():
    attacker_result = {}
    for unitTypeName, unitType in gameConfig['units'].items():
        attacker_result[unitTypeName] = {}
        for unitName, unitInfo in unitType.items():
            attacker_result[unitTypeName][unitName] = {
                'quantity' : 0,
                'lost' : 0
            }
    return attacker_result


def getResults(diff, date, attacker_info, defender_info, casualty_rate=None):
    if(diff>0): #attacker wins

        #Calculation of attacker losses
        attacker_result = createEmptyDictionaryForBattleReport()

        numberOfUnits = 0
        for unitTypeName, unitType in attacker_info['troops'].items():
            for unitName, unitQuantity in unitType.items():
                if(unitQuantity>0): 
                    numberOfUnits+=1
                    attacker_result[unitTypeName][unitName]['quantity'] = unitQuantity
        
        casualty_rate_net = float(casualty_rate) / float(numberOfUnits)

        for unitTypeName, unitType in attacker_info['troops'].items():
            for unitName, unitQuantity in unitType.items():
                if(unitQuantity>0): 
                    numberOfUnits+=1
                    attacker_result[unitTypeName][unitName]['lost'] = math.ceil(unitQuantity * casualty_rate_net)


        #Calculation of defender losses
        defender_result = createEmptyDictionaryForBattleReport()

        for unitTypeName, unitType in defender_info['troops'].items():
            for unitName, unitQuantity in unitType.items():
                if(unitQuantity>0): 
                    defender_result[unitTypeName][unitName]['quantity'] = unitQuantity
                    defender_result[unitTypeName][unitName]['lost'] = unitQuantity

        result = {
            'attacker' : {
                'user_id' : attacker_info['user_id'],
                'village_id' : attacker_info['village_id'],
                'units_result' : attacker_result,
                'result' : 'won'
            },
            'defender' : {
                'user_id' : defender_info['user_id'],
                'village_id' : defender_info['village_id'],
                'units_result' : defender_result,
                'result' : 'lost'
            }
        }

        return result

    elif(diff<0): #defender wins

        #Calculation of defender losses
        defender_result = createEmptyDictionaryForBattleReport()

        numberOfUnits = 0
        for unitTypeName, unitType in defender_info['troops'].items():
            for unitName, unitQuantity in unitType.items():
                if(unitQuantity>0): 
                    numberOfUnits+=1
                    defender_result[unitTypeName][unitName]['quantity'] = unitQuantity
        
        casualty_rate_net = float(casualty_rate) / float(numberOfUnits)

        for unitTypeName, unitType in defender_info['troops'].items():
            for unitName, unitQuantity in unitType.items():
                if(unitQuantity>0): 
                    numberOfUnits+=1
                    defender_result[unitTypeName][unitName]['lost'] = math.ceil(unitQuantity * casualty_rate_net)


        #Calculation of attacker losses
        attacker_result = createEmptyDictionaryForBattleReport()

        for unitTypeName, unitType in attacker_info['troops'].items():
            for unitName, unitQuantity in unitType.items():
                if(unitQuantity>0): 
                    attacker_result[unitTypeName][unitName]['quantity'] = unitQuantity
                    attacker_result[unitTypeName][unitName]['lost'] = unitQuantity

        result = {
            'attacker' : {
                'user_id' : attacker_info['user_id'],
                'village_id' : attacker_info['village_id'],
                'units_result' : attacker_result,
                'result' : 'lost'
            },
            'defender' : {
                'user_id' : defender_info['user_id'],
                'village_id' : defender_info['village_id'],
                'units_result' : defender_result,
                'result' : 'won'
            }
        }
        print("defender won")

        return result

    else: #nobody wins
        print("nobody won")

# def getUsernameByUserID(user_id):
#     players_ref = db.collection('players')
#     return players_ref.document(user_id).get({'username'}).to_dict()['username']

# def getVillagenameByVillageID(village_id):
#     villages_ref = db.collection('villages')
#     return villages_ref.document(village_id).get({'villageName'}).to_dict()['villageName']


from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.breadth_first import BreadthFirstFinder

def find_path(data, A, B):
    grid = Grid(matrix=data)
    finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
    A['x'] = int(A['x']/16)
    A['y'] = int(A['y']/16)
    B['x'] = int(B['x']/16)
    B['y'] = int(B['y']/16)

    if A['x'] < B['x']:
        start = grid.node(A['x'], A['y'])
        end = grid.node(B['x'], B['y'])
    elif A['x'] > B['x']:
        end = grid.node(A['x'], A['y'])
        start = grid.node(B['x'], B['y'])
    else: 
        if A['y'] < B['y']:
            start = grid.node(A['x'], A['y'])
            end = grid.node(B['x'], B['y'])
        elif A['y'] > B['y']:
            print(A, B)
            end = grid.node(A['x'], A['y'])
            start = grid.node(B['x'], B['y'])
        else:
            return ValueError("Can't calculate path from A to B when A==B")


    path, runs = finder.find_path(start, end, grid)
    # print('operations:', runs, 'path length:', len(path))
    # print(grid.grid_str(path=path, start=start, end=end))
    new_path = [(point[0]*16, point[1]*16) for point in path]
    return new_path

def convert_1d_to_2d_arr(data, height, width):
    data = np.array(data)
    data = data.reshape(height, width)
    return list(data)

def calculate_map_pathfinding(source, target, layer='land'):
    map_data = get_map_data()
    map_data = convert_1d_to_2d_arr(map_data[layer], 64, 128)
    path = find_path(map_data, source, target)
    
    return path