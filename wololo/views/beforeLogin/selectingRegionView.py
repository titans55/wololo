from django.shortcuts import render, redirect
from django.http import JsonResponse
from wololo.initFirestore import get_db, get_auth
from wololo.firebaseUser import firebaseUser
from wololo.commonFunctions import getGameConfig
import urllib.request
import urllib.error

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required


db = get_db()
auth = get_auth()
gameConfig = getGameConfig()


@login_required
def selectRegionOnFirstLoginView(request):
    user_id = request.user.id
    userInfo = db.collection('players').document(user_id).get()._data
    if userInfo['regionSelected'] is True :
        return redirect('myVillage')

    return render(request, "firstLogin/selectRegion.html")

@login_required
def selectingRegion(request):
    user_id = request.user.id
    userInfo = db.collection('players').document(user_id).get()._data
    if userInfo['regionSelected'] is True :
        return redirect('myVillage')
    
    selectedRegion = request.POST.get("selectedRegion")
    if selectedRegion != '':
        print(selectedRegion)
        allVillages = db.collection('villages').get()
        emptyVillages = []
        for village in allVillages:
            if village._data['playerName'] == '' and village._data['region'] == selectedRegion:
                emptyVillages.append(village)
        import random
        firstVillage = random.choice(emptyVillages)
        print("selected")
        firstVillage._data['id'] = firstVillage.reference.id
        print(firstVillage._data['id'])
        now = datetime.datetime.now()
        villageInfo = {
            "villageName" : 'new Village',
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
                    #     "movementType" : "Attack/Support",
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
                    #     "movementType" : "Attack/Support",
                    #     "arrivalTime" : "timestamp",
                    #     "troops": {
                    #         "infantry" :  {
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
                    #   }
                    #}
                }
            }
        }
        db.collection('players').document(user_id).collection('villages').document(firstVillage._data['id']).set(villageInfo)
        db.collection('villages').document(firstVillage._data['id']).update(
            {
                'user_id': user_id,
                'playerName':userInfo['username'],
                'villageName':'Yigidin Harman Oldugu Yer'
            }
        )
        db.collection('players').document(user_id).update({'regionSelected' : True})
    return redirect('myVillage')