from .initFirestore import get_db
from .commonFunctions import getGameConfig
import os
import json
import pytz, datetime
from celery import current_app
from wololo.helperFunctions import setSumAndLastInteractionDateOfResource, calculatePointsForPlayer, getUsernameByUserID, getVillagenameByVillageID
from google.cloud.firestore_v1beta1 import ArrayRemove, ArrayUnion
from django.core.serializers.json import DjangoJSONEncoder
from dateutil import parser

db = get_db()
gameConfig = getGameConfig()
class firebaseUser():

    refreshVillages = False #change this true to refresh villages to level 1 of logged in user

    def __init__(self, id):
        self.id = id
        self.initUser()

    def update(self):
        self.initUser()
        
    def initUser(self):
        villages = db.collection('players').document(self.id).collection('villages').get()
        myVillages = []
        numberOfVillages = 0
        for village in villages:
            now = datetime.datetime.now()
            if(self.refreshVillages):
                db.collection('players').document(self.id).collection('villages').document(village.reference.id).set(
                    {   
                        "villageName" : 'Village -' + str(numberOfVillages),
                        "buildings" : {
                            "townCenter" : {
                                "level" : "1",
                                "upgrading" : {
                                    "state": False,
                                    "time" : {
                                        "startedUpgradingAt" : now,
                                        "willBeUpgradedAt" : now 
                                    },
                                    "task_id" : ''
                                }
                            },
                            "barracks" : {
                                "level" : "0",
                                "upgrading" : {
                                    "state": False,
                                    "time" : {
                                        "startedUpgradingAt" : now,
                                        "willBeUpgradedAt" : now 
                                    },
                                    "task_id" : ''
                                }
                            },
                            "stable" : {
                                "level" : "0",
                                "upgrading" : {
                                    "state": False ,
                                    "time" : {
                                        "startedUpgradingAt" : now,
                                        "willBeUpgradedAt" : now 
                                    },
                                    "task_id" : ''
                                }
                            },
                            "workshop" : {
                                "level" : "0",
                                "upgrading" : {
                                    "state": False ,
                                    "time" : {
                                        "startedUpgradingAt" : now,
                                        "willBeUpgradedAt" : now 
                                    },
                                    "task_id" : ''
                                }
                            },
                            "storage" : {
                                "level" : "1",
                                "upgrading" : {
                                    "state": False ,
                                    "time" : {
                                        "startedUpgradingAt" : now,
                                        "willBeUpgradedAt" : now 
                                    },
                                    "task_id" : ''
                                }
                            },
                            "farm" : {
                                "level" : "1",
                                "upgrading" : {
                                    "state": False ,
                                    "time" : {
                                        "startedUpgradingAt" : now,
                                        "willBeUpgradedAt" : now 
                                    },
                                    "task_id" : ''
                                }
                            },
                            "resources" : {
                                "woodCamp" : {
                                    "lastInteractionDate" : now,
                                    "level" : "0",
                                    "sum" : 0,
                                    "upgrading" : {
                                        "state": False ,
                                        "time" : {
                                            "startedUpgradingAt" : now,
                                            "willBeUpgradedAt" : now 
                                        },
                                        "task_id" : ''
                                    }
                                },
                                "ironMine" : {
                                    "lastInteractionDate" : now,
                                    "level" : "0",
                                    "sum" : 0,
                                    "upgrading" : {
                                        "state": False ,
                                        "time" : {
                                            "startedUpgradingAt" : now,
                                            "willBeUpgradedAt" : now 
                                        },
                                        "task_id" : ''
                                    }
                                },
                                "clayPit" : {
                                    "lastInteractionDate" : now,
                                    "level" : "0",
                                    "sum" : 0,
                                    "upgrading" : {
                                        "state": False ,
                                        "time" : {
                                            "startedUpgradingAt" : now,
                                            "willBeUpgradedAt" : now 
                                        },
                                        "task_id" : ''
                                    }
                                }
                            }
                        },
                        "troops" : {
                            "inVillage" : {
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
                            },
                            "onMove" : {
                                # 'tsk_id' : {
                                #     "from" : "fromVillageID",
                                #     "to" : "targetVillageID",
                                #     "movementType" : "attack/support",
                                #     "state" : "going/returning",
                                #     "arrivalTime" : "timestamp",
                                #     "troops": {
                                #         "infantry": {
                                #             "Spearman" : 0,
                                #             "Swordsman" : 0,
                                #             "Axeman" : 0,
                                #             "Archer" : 0
                                #         },
                                #         "cavalry" : {
                                #             "Scout" : 0,
                                #             "Light Cavalry": 0,
                                #             "Heavy Cavalry" : 0
                                #         },
                                #         "siegeWeapons" : {
                                #             "Ram" : 0,
                                #             "Catapult": 0
                                #         }
                                #     }
                                # }
                            },
                            "total" : {
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
                            },
                            "trainingQueue" : {
                                "infantry" : [],
                                "cavalry" : [],
                                "siegeWeapons" : [],
                                "folkHero" : []
                            },
                            "incomingStrangerTroops" : {
                                # 'tsk_id' : {
                                #     "from" : "fromVillageID",
                                #     "to" : "targetVillageID",
                                #     "movementType" : "attack/support",
                                #     "arrivalTime" : "timestamp",
                                #     }
                                # }
                            }
                        }
                    }
                )
                calculatePointsForPlayer(self.id)
            # print(village)
            village._data['index'] = numberOfVillages 
            village._data['id'] = village.reference.id
            village._data['buildings']['resources']['woodCamp']['lastInteractionDate'] = str(village._data['buildings']['resources']['woodCamp']['lastInteractionDate'])
            village._data['buildings']['resources']['ironMine']['lastInteractionDate'] = str(village._data['buildings']['resources']['ironMine']['lastInteractionDate'])
            village._data['buildings']['resources']['clayPit']['lastInteractionDate'] = str(village._data['buildings']['resources']['clayPit']['lastInteractionDate'])

            for buildingName, building in village._data['buildings'].items():
                if buildingName == 'resources': 
                    for resource in building:
                        village._data['buildings']['resources'][resource]['upgrading']['state'] = 'true' if village._data['buildings']['resources'][resource]['upgrading']['state'] else 'false'
                        village._data['buildings']['resources'][resource]['upgrading']['time']['startedUpgradingAt'] = str(village._data['buildings']['resources'][resource]['upgrading']['time']['startedUpgradingAt'])
                        village._data['buildings']['resources'][resource]['upgrading']['time']['willBeUpgradedAt'] = str(village._data['buildings']['resources'][resource]['upgrading']['time']['willBeUpgradedAt'])
                else :
                    village._data['buildings'][buildingName]['upgrading']['state'] = 'true' if village._data['buildings'][buildingName]['upgrading']['state'] else 'false'
                    village._data['buildings'][buildingName]['upgrading']['time']['startedUpgradingAt'] = str(village._data['buildings'][buildingName]['upgrading']['time']['startedUpgradingAt'])
                    village._data['buildings'][buildingName]['upgrading']['time']['willBeUpgradedAt'] = str(village._data['buildings'][buildingName]['upgrading']['time']['willBeUpgradedAt'])

            village._data['troops']['trainingQueue'] = json.loads(json.dumps(village._data['troops']['trainingQueue'], cls=DjangoJSONEncoder))
            village._data['troops']['onMove'] = json.loads(json.dumps(village._data['troops']['onMove'], cls=DjangoJSONEncoder))
            village._data['troops']['incomingStrangerTroops'] = json.loads(json.dumps(village._data['troops']['incomingStrangerTroops'], cls=DjangoJSONEncoder))

            temp = village._data['buildings']
            village._data['buildings'] = {}
            for building in gameConfig['buildings'].keys():
                if building == 'resources':
                    resources = {}
                    for resourceBuilding in gameConfig['buildings']['resources'].keys():
                        resources[resourceBuilding] = temp['resources'][resourceBuilding]
                    village._data['buildings']['resources'] = resources
                else: 
                    village._data['buildings'][building] = temp[building]
        
            # print(village._data['buildings'])
                
            myVillages.append(village._data)
            numberOfVillages += 1

        self.myVillages = myVillages
        self.numberOfVillages = numberOfVillages
        self.regionSelected = db.collection('players').document(self.id).get({'regionSelected'}).to_dict()['regionSelected']
        self.unviewedReportExists = self.getUnviewedReportExists()

    def upgradeBuilding(self, village_id, building_path):
        village_ref = db.collection('players').document(self.id).collection('villages').document(village_id)
        village = village_ref.get().to_dict()
        if('.' in building_path):
            upgrade_level_to = str(int(village['buildings']['resources'][building_path.split('.')[1]]['level']) + 1)
        else:
            upgrade_level_to = str(int(village['buildings'][building_path]['level']) + 1)
        
        village_ref.update({
            'buildings.'+building_path+'.upgrading.state' : False,
            'buildings.'+building_path+'.level' : upgrade_level_to
        })

        if('.' in building_path):

            now = datetime.datetime.now(pytz.utc)
            newSum = self.getCurrentResource(village_id, building_path.split('.')[1])
           
            village_ref.update({
                'buildings.'+building_path+'.sum' : newSum,
                'buildings.'+building_path+'.lastInteractionDate' : now
            })
            print("sueccesfullll")

    def setUpgradingTimeAndState(self, village_id, building_path, reqiured_time, task_id, now):
        user_id = self.id
        village = db.collection('players').document(user_id).collection('villages').document(village_id)
        # now = datetime.datetime.now()
        # now = datetime.datetime.fromtimestamp(now)
        willEnd = now+datetime.timedelta(0, reqiured_time)
    
        village.update({
            'buildings.'+building_path+'.upgrading.time.startedUpgradingAt' : now,
            'buildings.'+building_path+'.upgrading.time.willBeUpgradedAt' : willEnd,
            'buildings.'+building_path+'.upgrading.state' : True,
            'buildings.'+building_path+'.upgrading.task_id' : task_id
        })


    def cancelUpgrading(self, village_id, building_path, now):
        task_id_to_revoke = self.getBuildingUpgradeTaskId(village_id, building_path)
        current_app.control.revoke(task_id_to_revoke)
        print("task is revoked")
        user_id = self.id
        village = db.collection('players').document(user_id).collection('villages').document(village_id)
        village.update({
            'buildings.'+building_path+'.upgrading.state' : False
        })
        
        
        capacity = gameConfig['buildings']['storage']['capacity'][str(self.getBuildingLevel(village_id, 'storage'))]

        oldWood = self.getCurrentResource(village_id, 'woodCamp')
        oldIron = self.getCurrentResource(village_id, 'ironMine')
        oldClay = self.getCurrentResource(village_id, 'clayPit')

        if '.' in building_path : 
            upgrade_levelTo = str(int(self.getBuildingLevel(village_id, building_path)) + 1)
            returned_clay = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['clay'] *20/100
            returned_iron = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['iron'] *20/100
            returned_wood = gameConfig['buildings']['resources'][building_path.split('.')[1]]['upgradingCosts'][upgrade_levelTo]['wood'] *20/100
        else :
            upgrade_levelTo = str(int(self.getBuildingLevel(village_id, building_path)) + 1)
            returned_clay = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['clay'] *20/100
            returned_iron = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['iron'] *20/100
            returned_wood = gameConfig['buildings'][building_path]['upgradingCosts'][upgrade_levelTo]['wood'] *20/100

        newWood = oldWood + returned_wood if oldWood + returned_wood < capacity else capacity
        newIron = oldIron + returned_iron if oldIron + returned_iron < capacity else capacity
        newClay = oldClay + returned_clay if oldClay + returned_clay < capacity else capacity
        #20% of cost


        setSumAndLastInteractionDateOfResource(self.id, village_id, 'woodCamp', newWood, now)
        setSumAndLastInteractionDateOfResource(self.id, village_id, 'ironMine', newIron, now)
        setSumAndLastInteractionDateOfResource(self.id, village_id, 'clayPit', newClay, now)

    




    def getCurrentResource(self, village_id, resourceBuilding):

        now = datetime.datetime.now(pytz.utc)
        village = self.getVillageById(village_id)
        resourceSum = village['buildings']['resources'][resourceBuilding]['sum']
        resourceLevel = village['buildings']['resources'][resourceBuilding]['level']
        resourceLastInteractionDate = parser.parse(village['buildings']['resources'][resourceBuilding]['lastInteractionDate'])
        hourlyProductionByLevel = gameConfig['buildings']['resources'][resourceBuilding]['hourlyProductionByLevel'][resourceLevel]
        totalHoursOfProduction = (now-resourceLastInteractionDate).total_seconds() / 60 / 60
        totalCurrentResource = (totalHoursOfProduction * hourlyProductionByLevel) + resourceSum
        if totalCurrentResource >= gameConfig['buildings']['storage']['capacity'][village['buildings']['storage']['level']]:
            totalCurrentResource = gameConfig['buildings']['storage']['capacity'][village['buildings']['storage']['level']]
        return int(totalCurrentResource)

    def getVillageById(self, village_id):
        for village in self.myVillages:
            if(village['id'] == village_id):
                return village
        
        return False


    def getBuildingLevel(self, village_id, building_path):
        villageDict = db.collection('players').document(self.id).collection('villages').document(village_id).get().to_dict()
        if('.' in building_path):
            return villageDict['buildings']['resources'][building_path.split('.')[1]]['level']
        else:
            return villageDict['buildings'][building_path]['level']

    
    def getBuildingUpgradeTaskId(self, village_id, building_path):
        villageDict = self.getVillageById(village_id)
        if('.' in building_path):
            return villageDict['buildings']['resources'][building_path.split('.')[1]]['upgrading']['task_id']
        else:
            return villageDict['buildings'][building_path]['upgrading']['task_id']

    def getUnitsLeft(self, village_id, unitType, unitName):
        #villageDict = self.getVillageById(village_id)
        #return villageDict['troops']['trainingUnits'][unitType][unitName]['timeAndQuantity']['unitsLeft']

        unitsLeft = db.collection('players').document(self.id).collection('villages').document(village_id).get({'troops.trainingQueue.'+ unitType}).to_dict()['troops']['trainingQueue'][unitType][0]['unitsLeft']
        return unitsLeft

    def setUnitsLeft(self, village_id, unitType, unitName, newUnitsLeft):
        village_ref = db.collection('players').document(self.id).collection('villages').document(village_id)
        village_ref.update({
            'troops.trainingUnits.'+ unitType +'.'+ unitName +'.timeAndQuantity.unitsLeft' : newUnitsLeft,
        })
    
    def setUnitsTrainingState(self, village_id, unitType, unitName, newState):
        village_ref = db.collection('players').document(self.id).collection('villages').document(village_id)
        village_ref.update({
            'troops.trainingUnits.'+ unitType +'.'+ unitName +'.state' : newState,
        })

    def getTotalUnitsQuantity(self, village_id, unitType, unitName):
        villageDict = self.getVillageById(village_id)
        return villageDict['troops']['total'][unitType][unitName]

    def getInVallageUnitsQuantity(self, village_id, unitType, unitName):
        villageDict = self.getVillageById(village_id)
        return villageDict['troops']['inVillage'][unitType][unitName]

    def trainUnit(self, village_id, unitType, unitName):
        village_ref = db.collection('players').document(self.id).collection('villages').document(village_id)
        unitsLeft = self.getUnitsLeft(village_id, unitType, unitName)
        totalUnitsQuantity = self.getTotalUnitsQuantity(village_id, unitType, unitName)
        inVillageUnitsQuantity = self.getInVallageUnitsQuantity(village_id, unitType, unitName)

        unitsLeft -= 1 if unitsLeft > 0 else 0
        totalUnitsQuantity += 1
        inVillageUnitsQuantity += 1

        ###
        village_ref.update({
            'troops.total.'+ unitType+'.'+ unitName : totalUnitsQuantity,
            'troops.inVillage.'+ unitType+'.'+ unitName : inVillageUnitsQuantity,
        })
        ###
        allQueue = db.collection('players').document(self.id).collection('villages').document(village_id).get({'troops.trainingQueue.'+ unitType}).to_dict()['troops']['trainingQueue'][unitType]

        print('unitsLeft => ', unitsLeft)
        if unitsLeft == 0 :
            village_ref.update({
                'troops.trainingQueue.'+unitType : ArrayRemove(
                    [allQueue[0]]
                )
            })
        else:
            allQueue[0]['unitsLeft'] = unitsLeft
            village_ref.update({ 
                'troops.trainingQueue.'+unitType : allQueue
            })
            
    def addToTrainingQueue(self, village_id, chain_id, unitType, unitName, unitsLeft, startedAt, willEndAt):

        village_ref = db.collection('players').document(self.id).collection('villages').document(village_id)
        village_ref.update({
            'troops.trainingQueue.'+unitType : ArrayUnion([{
                'chain_id': chain_id,
                'unitName' : unitName,
                'unitsLeft' : unitsLeft,
                'startedAt' : startedAt,
                'willEndAt' : willEndAt
            }])
        })


    def checkTrainingQueueReturnLastOneIfExists(self, village_id, unitType):

        trainingQueue = db.collection('players').document(self.id).collection('villages').document(village_id).get({'troops.trainingQueue.'+ unitType}).to_dict()['troops']['trainingQueue'][unitType]
    
        return False if len(trainingQueue) == 0 else trainingQueue[-1]


    def weHaveResourcesToTrainUnit(self, village_id, unitType, unitName, numberOfUnitsToTrain):

        currentWood = self.getCurrentResource(village_id, 'woodCamp')
        currentIron = self.getCurrentResource(village_id, 'ironMine')
        currentClay = self.getCurrentResource(village_id, 'clayPit')

        reqiuredWood = gameConfig['units'][unitType][unitName]['Cost']['Wood'] * numberOfUnitsToTrain
        reqiuredIron = gameConfig['units'][unitType][unitName]['Cost']['Iron'] * numberOfUnitsToTrain
        reqiuredClay = gameConfig['units'][unitType][unitName]['Cost']['Clay'] * numberOfUnitsToTrain

        if(currentWood >= reqiuredWood and currentIron >= reqiuredIron and currentClay >= reqiuredClay):

            return True
        else:
            return False

    def getAllInVallageUnits(self, village_id):
        villageDict = self.getVillageById(village_id)
        return villageDict['troops']['inVillage']

    def addOnMoveTroops(self, task_id, movementDetails, troops):
        
        village_ref = db.collection('players').document(self.id).collection('villages').document(movementDetails['home_village_id'])
        inVillageTroops = village_ref.get({'troops.inVillage'}).to_dict()['troops']['inVillage']
        for unitTypeName, unitType in inVillageTroops.items():
            for unitName, unit in unitType.items():
                inVillageTroops[unitTypeName][unitName] -= troops[unitTypeName][unitName]

        print(inVillageTroops)
        village_ref.update({
            'troops.onMove' : {
                task_id : {
                    "countdown" : movementDetails['countdown'],
                    "home_village_id" : movementDetails['home_village_id'],
                    "target_village_id" : movementDetails['target_village_id'],
                    "movementType" :  movementDetails['movementType'], #attack/support
                    "state" : movementDetails['state'], #going/returning
                    "arrivalTime" : movementDetails['arrivalTime'],
                    "troops": {
                        "infantry": {
                            "Spearman" : troops['infantry']['Spearman'],
                            "Swordsman" : troops['infantry']['Swordsman'],
                            "Axeman" : troops['infantry']['Axeman'],
                            "Archer" : troops['infantry']['Archer']
                        },
                        "cavalry" : {
                            "Scout" : troops['cavalry']['Scout'],
                            "Light Cavalry": troops['cavalry']['Light Cavalry'],
                            "Heavy Cavalry" : troops['cavalry']['Heavy Cavalry']
                        },
                        "siegeWeapons" : {
                            "Ram" : troops['siegeWeapons']['Ram'],
                            "Catapult": troops['siegeWeapons']['Catapult']
                        }
                    }
                }
            },
            'troops.inVillage' : inVillageTroops
        })

    def addIncomingStrangerTroops(self, task_id, movementDetails):
        village_ref = db.collection('players').document(self.id).collection('villages').document(movementDetails['target_village_id'])
        village_ref.update({
            'troops.incomingStrangerTroops' : {
                task_id : {
                    "countdown" : movementDetails['countdown'],
                    "home_village_id" : movementDetails['home_village_id'],
                    "target_village_id" : movementDetails['target_village_id'],
                    "movementType" :  movementDetails['movementType'], #attack/support
                    "arrivalTime" : movementDetails['arrivalTime']
                }
            }
        })

    def insertReport(self, reportType, date, content):
        player_ref = db.collection('players').document(self.id)

        if(reportType=='battle'):
            if(content['attacker']['user_id'] == self.id): 
                if(content['attacker']['result'] == 'lost'):
                    content['defender']['units_result'] == 'unknown'
            
            content['attacker']['username'] = getUsernameByUserID(content['attacker']['user_id'])
            content['attacker']['villageName'] = getVillagenameByVillageID(content['attacker']['village_id'])
            content['defender']['username'] = getUsernameByUserID(content['defender']['user_id'])
            content['defender']['villageName'] = getVillagenameByVillageID(content['defender']['village_id'])


            newReport = {
                'type' : reportType,
                'date' : date, 
                'viewed' : False,
                'content' : content
            }

            player_ref.update({
                'reports': ArrayUnion([
                    newReport
                ]),
                'unviewedReportExists' : True
            })

    def getReports(self):

        reports = json.loads(json.dumps(db.collection('players').document(self.id).get({'reports'}).to_dict()['reports'], cls=DjangoJSONEncoder))
        
        # for report in reports:
        #     if report['type']=='battle':
        #         report['content']['attacker']['username'] = getUsernameByUserID(report['content']['attacker']['user_id'])
        #         report['content']['attacker']['villageName'] = getVillagenameByVillageID(report['content']['attacker']['village_id'])
        #         report['content']['defender']['username'] = getUsernameByUserID(report['content']['defender']['user_id'])
        #         report['content']['defender']['villageName'] = getVillagenameByVillageID(report['content']['defender']['village_id'])
        
        return reports


    def setUnviewedReportExists(self, boolean):
        player_ref = db.collection('players').document(self.id)
        player_ref.update({
            'unviewedReportExists' : boolean
        })

    def getUnviewedReportExists(self):
        
        return db.collection('players').document(self.id).get({'unviewedReportExists'}).to_dict()['unviewedReportExists']
        
    def setReports(self, reports):
        player_ref = db.collection('players').document(self.id)
        player_ref.update({
            'reports' : reports
        })