from __future__ import absolute_import, unicode_literals
from celery import Celery
import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
import pytz
from DjangoPostgresProject import settings
import django
django.setup()
from wololo.helperFunctions import calculate_points_for_village, getUserIdByVillageId, getResults
from wololo.commonFunctions import getGameConfig, getVillageIndex, default_fresh_troops_dict
from random import randint
# from google.cloud.firestore_v1beta1 import ArrayRemove, ArrayUnion, DELETE_FIELD
from wololo.models import Villages, Users, TroopMovements, BattleResults, Reports, BattleReports
from django.db import transaction

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

gameConfig = getGameConfig()

# set the default Django settings module for the 'celery' program.

app = Celery('tasks', broker='pyamqp://guest@localhost//',backend='amqp://guest@localhost//')

# Load task modules from all registered Django app configs.

@app.task(name='wololo.tasks.add_village')
def add_village(user_id, user_name, village_name):
    village = {
        "coords":{
            "x": 123,
            "y": 200
        },
        "playerName": user_name,
        "user_id": user_id,
        "villageName": village_name
    }
    db.collection("villages").add(village)
    return True


import urllib.request

@app.task(name='wololo.tasks.upgrade_building')
def schedule_upgrade_building(user_id, village_id, building_path, upgrade_level):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoPostgresProject.settings'
    channel_layer = get_channel_layer()

    user = Users.objects.get(id=user_id)
    user.upgrade_building(village_id, building_path)


    my_villages = user.get_my_villages()
    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))

    village = None
    print("task village_id", village_id)
    for vil in my_villages:
        print("vil id", vil['village_id'])
        if int(vil['village_id']) == int(village_id):
            village = vil
            print("adsada")
            break
    print(my_villages)
    newBuildings = village['buildings']
    notifyData = {
        'messageType': 'upgradeBuilding',
        'target': building_path,
        'newBuildings' : newBuildings,
        'villageId' : village_id
    }    

    async_to_sync ( channel_layer. group_send ) (
        str(user_id) , { "type" : "notify.user" , "json" : notifyData }
    )

    calculate_points_for_village(village_id) # TODO put this into another task later
        
    return True

@app.task(bind=True, name='wololo.tasks.train_unit')
def train_unit(self, user_id, village_id, unit_type, unit_name):
    
    user = Users.objects.get(id=user_id)
    vil = Villages.objects.get(id=village_id)
    if vil.get_units_left(unit_type, unit_name) == 0: ##if unitsLeft is 0 
        print("cancelled unit")
        self.request.chain = None #For cancelling training units
    else :
        os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoPostgresProject.settings'
        channel_layer = get_channel_layer()
        
        vil.train_unit(unit_type, unit_name)

        notifyData = {
            'messageType': 'trainUnit',
            'unitType': unit_type,
            'unitName': unit_name,
            'villageId' : village_id
        }    

        async_to_sync ( channel_layer. group_send ) (
            str(user_id) , { "type" : "notify.user" , "json" : notifyData }
        )
#battle occures in that function
@app.task(bind=True, name='wololo.tasks.attack')
def attack(self, attacker_village_id, defender_village_id, attacker_troops):
    with transaction.atomic():
        now = datetime.datetime.now(pytz.utc)
        current_task_id = self.request.id

        attacker_village = Villages.objects.get(id=attacker_village_id)
        attacker_user = attacker_village.user
        attacker_village_troops = attacker_village.village_troops
        attacker_total = attacker_village_troops.total_troops_quantity_json

        defender_village = Villages.objects.get(id=defender_village_id)
        defender_user = defender_village.user
        defender_village_troops = defender_village.village_troops
        defender_troops = defender_village_troops.in_village_troops_quantity_json

        #calculation of attack_force#
        attack_force = 0
        cavalry_attack_force = 0
        total_attacker_other_units = 0
        total_attacker_cavalry_units = 0

        for unit_type_name, unit_type in attacker_troops.items():
            for unit_name, unit_quantity in unit_type.items():
                unit_quantity = int(unit_quantity)
                if(unit_type_name=='cavalry'):
                    cavalry_attack_force += int(unit_quantity * gameConfig['units'][unit_type_name][unit_name]['Skills']['Attack'])
                    total_attacker_cavalry_units += unit_quantity
                else:
                    attack_force += int(unit_quantity * gameConfig['units'][unit_type_name][unit_name]['Skills']['Attack'])
                    total_attacker_other_units += unit_quantity

        total_attacker_units = total_attacker_other_units + total_attacker_cavalry_units
        attacker_other_units_perc = 100 * float(total_attacker_other_units)/float(total_attacker_units)
        attacker_cavalry_units_perc = float(100) - attacker_other_units_perc

        #calculation of defend_force#
        defend_force = 0
        cavalry_defend_force = 0


        for unit_type_name, unit_type in defender_troops.items():
            for unit_name, unit_quantity in unit_type.items():
                unit_quantity = int(unit_quantity)
                defend_force += int((unit_quantity*(attacker_other_units_perc/100))*gameConfig['units'][unit_type_name][unit_name]['Skills']['Defence'])
                cavalry_defend_force += int((unit_quantity*(attacker_cavalry_units_perc/100))*gameConfig['units'][unit_type_name][unit_name]['Skills']['Cavalry Defence'])
        ##

        print(attacker_other_units_perc, "attacker_other_units_perc")
        print(attacker_cavalry_units_perc, "attacker_cavalry_units_perc")

        print(attack_force, " attack force")
        print(cavalry_attack_force, " cavalry attack force")

        print(defend_force, " defend force")
        print(cavalry_defend_force, " cavalry defend force")

        total_attack_force = attack_force + cavalry_attack_force
        total_defend_force = defend_force + cavalry_defend_force
        ## luck (for attacker)
        luck = randint(-25, 25)
        print(luck, " luck")
        total_attack_force += int(total_attack_force*(luck/100.0))

        ## wall (do the same thing for defender)

        ##

        attacker_info = {
            'user_id' : attacker_user.id,
            'village_id' : attacker_village_id,
            'troops' : attacker_troops
        }
        defender_info = {
            'user_id' : defender_user.id,
            'village_id' : defender_village_id,
            'troops' : defender_troops
        }

        diff = total_attack_force - total_defend_force
        print(diff, " diff")
        if(diff>0):
            print("attacker won")
            casualty_rate = total_defend_force / total_attack_force
            print(casualty_rate, "casualty rate for attacker")
        elif(diff<0):
            print("defender won")
            casualty_rate = total_attack_force / total_defend_force
            print(casualty_rate, "casualty rate for defender")
        else:
            ##everyone dies
            casualty_rate = 1
            print("nobody won wtf")

        report_content = getResults(diff, now, attacker_info, defender_info, casualty_rate)
        
        #attacker
        if report_content['attacker']['result'] == 'won':
            print(report_content['attacker']['user_id'], report_content['attacker']['village_id'])
            # village_ref = db.collection('players').document(report_content['attacker']['user_id']).collection('villages').document(report_content['attacker']['village_id'])
            # cntdwn = village_ref.get({'troops.onMove'}).to_dict()['troops']['onMove'][current_task_id]['countdown']
            incoming_troop_movement = TroopMovements.objects.get(task_id=current_task_id)
            cntdwn = incoming_troop_movement.movement_duration_seconds

            returning_troops = default_fresh_troops_dict()

            #LEFT IN HEREEEEEEEEEEEEEEEE~~~~~~~~~~~~~~~~~~~~~~~~#########
            # total = village_ref.get({'troops.total'}).to_dict()['troops']['total']

            for unitTypeName, unitType in report_content['attacker']['units_result'].items():
                for unitName, unit in unitType.items():
                    if(unit['quantity']!=unit['lost']):
                        returning_troops[unitTypeName][unitName] = unit['quantity'] - unit['lost']
                    attacker_total[unitTypeName][unitName] -= unit['lost'] #calculating new total

            new_task_id = return_from_attack.apply_async((report_content['defender']['village_id'], report_content['attacker']['village_id'], returning_troops),countdown = cntdwn)
            new_task_id = new_task_id.id
            arrivalTime = now + datetime.timedelta(0, cntdwn)

            #delete attacker onMove, insert newOnMove(newtaskid), total
            incoming_troop_movement.delete()
            TroopMovements.objects.create(
                task_id=new_task_id,
                arrival_time=arrivalTime,
                movement_duration_seconds=cntdwn,
                moving_troops_json=returning_troops,
                movement_type='attack',
                state='returning',
                home_village=attacker_village,
                target_village=defender_village
            )
            attacker_village_troops.on_move_troops_quantity_json = returning_troops #TODO normalize onMove
            attacker_village_troops.save()
            # village_ref.update({
            #     'troops.onMove.'+current_task_id: DELETE_FIELD
            # })
            

            # village_ref.update({
            #     'troops.onMove': { 
            #         new_task_id : {
            #             "home_village_id" : report_content['attacker']['village_id'],
            #             "target_village_id" : report_content['defender']['village_id'],
            #             "movementType" :  'attack', #attack/support
            #             "state" : 'returning', #going/returning
            #             "arrivalTime" : arrivalTime,
            #             "troops": returning_troops
            #         }
            #     },
            #     'troops.total': total
            # })
            
        else:
            # village_ref = db.collection('players').document(report_content['attacker']['user_id']).collection('villages').document(report_content['attacker']['village_id'])
            
            # total = village_ref.get({'troops.total'}).to_dict()['troops']['total']


            for unitTypeName, unitType in report_content['attacker']['units_result'].items():
                for unitName, unit in unitType.items():
                    attacker_total[unitTypeName][unitName] -= unit['lost'] #calculating new total
            
            #delete attacker onMove, update total 
            attacker_village_troops.on_move_troops_quantity_json = default_fresh_troops_dict()
            attacker_village_troops.save()
            # village_ref.update({
            #     'troops.onMove.'+current_task_id: DELETE_FIELD,
            #     'troops.total': total
            # })
        # print("removed onMove from attacker")
        #defender
        # village_ref = db.collection('players').document(report_content['defender']['user_id']).collection('villages').document(report_content['defender']['village_id'])
        # total = village_ref.get({'troops.total'}).to_dict()['troops']['total']
        # inVillage = village_ref.get({'troops.inVillage'}).to_dict()['troops']['inVillage']

        for unitTypeName, unitType in report_content['defender']['units_result'].items():
            for unitName, unit in unitType.items():
                defender_troops[unitTypeName][unitName] -= unit['lost'] #calculating new inVillage

        #update defender inVillage, total, delete incomingStrangerTroops
        # village_ref.update({
        #     'troops.incomingStrangerTroops.' + current_task_id: DELETE_FIELD,
        #     'troops.inVillage' :inVillage,
        #     'troops.total': total
        # })
        # print("removed incomingStrangerTroops from defender")
        defender_village_troops.in_village_troops_quantity_json = defender_troops
        defender_village_troops.save()
        ### INSERT REPORTS ###
        attacker_battle_result = BattleResults.objects.create(
            quantity_and_losses_troops_json = report_content['attacker']['units_result'],
            result = report_content['attacker']['result']
        )
        defender_battle_result = BattleResults.objects.create(
            quantity_and_losses_troops_json = report_content['defender']['units_result'],
            result = report_content['defender']['result']
        )
        attacker_report = Reports.objects.create(
            type='battle',
            sended_to_user=attacker_user
        )
        defender_report = Reports.objects.create(
            type='battle',
            sended_to_user=defender_user
        )

        attacker_battle_report = BattleReports.objects.create(
            report=attacker_report,
            is_details_hidden=report_content['attacker']['result'] == 'lost',
            attacker=attacker_user,
            attacker_village=attacker_village,
            attacker_battle_result=attacker_battle_result,
            defender=defender_user,
            defender_village=defender_village,
            defender_battle_result=defender_battle_result
        )
        defender_battle_report = BattleReports.objects.create(
            report=defender_report,
            is_details_hidden=False,
            attacker=attacker_user,
            attacker_village=attacker_village,
            attacker_battle_result=attacker_battle_result,
            defender=defender_user,
            defender_village=defender_village,
            defender_battle_result=defender_battle_result
        )
   
        ## TODO send message to both attacker and defender clients


@app.task(bind=True, name='wololo.tasks.return_from_attack')
def return_from_attack(self, target_village_id, home_village_id, returning_troops):
    # user_id = getUserIdByVillageId(home_village_id)
    current_task_id = self.request.id

    # village_ref = db.collection('players').document(user_id).collection('villages').document(home_village_id)
    # inVillage = village_ref.get({'troops.inVillage'}).to_dict()['troops']['inVillage']

    home_village = Villages.objects.get(id=home_village_id)
    
    with transaction.atomic():
        for unitTypeName, unitType in returning_troops.items():
            for unitName, unit_quantity in unitType.items():
                home_village.village_troops.in_village_troops_quantity_json\
                    [unitTypeName][unitName] += unit_quantity
                home_village.village_troops.on_move_troops_quantity_json\
                    [unitTypeName][unitName] -= unit_quantity

        returning_troop_movement = TroopMovements.objects.get(task_id=current_task_id)

        returning_troop_movement.delete()
        home_village.village_troops.save()

        # for unitTypeName, unitType in returning_troops.items():
        #     for unitName, unit in unitType.items():
        #         inVillage[unitTypeName][unitName] += unit

        # village_ref.update({
        #     'troops.onMove.'+current_task_id: DELETE_FIELD,
        #     'troops.inVillage' : inVillage,
        # })
        print("removed onMove from attacker")

        print("TROOPS RETURNED HOME")
