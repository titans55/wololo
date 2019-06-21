import datetime
import json
import os
import dateutil.parser
import pytz
import pyrebase
from .initFirestore import get_db
from .commonFunctions import getGameConfig
import datetime
import math
from google.cloud.firestore_v1beta1 import ArrayRemove, ArrayUnion, DELETE_FIELD
from wololo.models import Users, VillageBuildings, ResourceBuildingDetails

db = get_db()

gameConfig = getGameConfig()





def setSumAndLastInteractionDateOfResource(user_id, village_id, resourceBuilding, newSum, now):

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


def getRequiredTimeForTrainUnits(village, unitType, unitName):

    reqiured_time = gameConfig['units'][unitType][unitName]['neededTrainingBaseTime']
    speedPercantageOfBarracks = gameConfig['buildings']['barracks']['trainingSpeed'][str(village['buildings']['barracks']['level'])]
    reqiured_time = int(reqiured_time - (reqiured_time * speedPercantageOfBarracks / 100 )) * 60 #seconds
    
    return reqiured_time

def calculatePointsForVillage(village_id):

    public_village_ref = db.collection('villages').document(village_id)
    public_village = public_village_ref.get().to_dict()
    user_id = public_village['user_id']
    village = db.collection('players').document(user_id).collection('villages').document(village_id).get().to_dict()

    calculatedPoints = 0
    for buildingName, building in village['buildings'].items():
        if buildingName == 'resources':
            for resourceBuildingName, resourceBuilding in building.items():
                pointOfBuilding = gameConfig['buildings']['resources'][resourceBuildingName]['pointByLevel'][resourceBuilding['level']]
                calculatedPoints += pointOfBuilding
        else:
            pointOfBuilding = gameConfig['buildings'][buildingName]['pointByLevel'][building['level']]
            calculatedPoints += pointOfBuilding

    # calculatedPoints = 5

    public_village_ref.update({
        'points': calculatedPoints
    })
    calculatePointsForPlayer(user_id)

def calculatePointsForPlayer(user_id):
    player_ref = db.collection('players').document(user_id)
    villages_ref = db.collection('villages')
    playersVillagesGenerator = player_ref.collection('villages').get()
    calculatedPoints = 0
    for village in playersVillagesGenerator: 
        villagePoints = villages_ref.document(village.reference.id).get({'points'}).to_dict()['points']      
        calculatedPoints+=villagePoints
    player_ref.update({
        'points': calculatedPoints
    })
    
from wololo.models import Users
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

def getPlayerInfo(player_id):
    players_ref = db.collection('players')
    villages_ref = db.collection('villages')
    playerInfo = players_ref.document(player_id).get().to_dict()
    playersVillages = []
    for village in villages_ref.get(): 
        print(village.reference.id)
        villageDict = village.to_dict()
        if(villageDict['user_id'] == player_id):
            villageDict['village_id'] = village.reference.id
            playersVillages.append(villageDict)
            
    playerInfo['playersVillages'] = playersVillages
    playerInfo['id'] = player_id
    return playerInfo            

def getVillageInfo(village_id):
    players_ref = db.collection('players')
    villages_ref = db.collection('villages')
    villageInfo = villages_ref.document(village_id).get().to_dict()
    villageInfo['village_id'] = village_id
    playerClan = players_ref.document(villageInfo['user_id']).get({'clan'}).to_dict()['clan']
    villageInfo['clan'] = playerClan
    return villageInfo

def getPublicVillages(firebaseUser):
    
    public_villages_ref = db.collection('villages')
    publicVillages = public_villages_ref.get()
    publicVillagesInfo = []
    for village in publicVillages:
        if(village._data['user_id']!=''):
            village._data['village_id'] = village.reference.id
            if(village._data['user_id'] == firebaseUser.id):
                village._data['owner'] = True
                for myVillage in firebaseUser.myVillages:
                    if (village._data['village_id'] == myVillage['id']):
                        myVillage['coords'] = {
                            'x' : village._data['coords']['x'],
                            'y' : village._data['coords']['y']
                        }
            publicVillagesInfo.append(village._data)

    return publicVillagesInfo

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

def getUsernameByUserID(user_id):
    players_ref = db.collection('players')
    return players_ref.document(user_id).get({'username'}).to_dict()['username']

def getVillagenameByVillageID(village_id):
    villages_ref = db.collection('villages')
    return villages_ref.document(village_id).get({'villageName'}).to_dict()['villageName']