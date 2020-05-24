from django.urls import reverse
from django.contrib.postgres.fields import JSONField
from django.db.models import AutoField
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import EmailField
from django.db.models import IntegerField
from django.db.models import PositiveIntegerField
from django.db.models import SmallIntegerField
from django.db.models import TextField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields
from django.contrib.auth.models import AbstractUser

from wololo.commonFunctions import default_fresh_troops_dict
from dateutil import parser
import pytz
import datetime
from wololo.commonFunctions import getGameConfig
gameConfig = getGameConfig()


class Users(AbstractUser):

    # Fields
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=30)
    is_region_selected = models.BooleanField(default=False)
    is_unviewed_reports_exists = models.BooleanField(default=False)
    username = models.CharField(max_length=15, unique=True)
    clan_id = models.SmallIntegerField(blank=True, null=True)
    number_of_villages = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_users_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_users_update', args=(self.pk,))

    def get_my_village(self, village):
        if not Villages.objects.filter(user_id=self.id, id=village.id).exists():
            raise Exception("You can only access to your own villages")

        village_dict = {
            'buildings': {
                'resources': {}
            },
            'villageName': village.village_name,
            'troops': {},
            'village_id': village.id,
            'coords': {
                'x': village.coords_x,
                'y': village.coords_y
            }
        }
        village_building_querysets = VillageBuildings.objects.filter(
            village_id=village)
        for village_building in village_building_querysets:
            if village_building.is_resource_building:
                rbd = village_building.resource_building_detail_id
                ud = village_building.upgrading_details_id
                village_dict['buildings']['resources'][village_building.building_name] = {
                    'level': village_building.level,
                    'sum': rbd.sum,
                    'lastInteractionDate': rbd.last_interaction_date,
                    'upgrading': {
                        'state': village_building.is_upgrading,
                        'task_id': ud.task_id if ud else None,
                        'time': {
                            'startedUpgradingAt': ud.started_upgrading_at if ud else None,
                            'willBeUpgradedAt': ud.will_be_upgraded_at if ud else None
                        }
                    }
                }
            else:
                ud = village_building.upgrading_details_id
                village_dict['buildings'][village_building.building_name] = {
                    'level': village_building.level,
                    'upgrading': {
                        'state': village_building.is_upgrading,
                        'task_id': ud.task_id if ud else None,
                        'time': {
                            'startedUpgradingAt': ud.started_upgrading_at if ud else None,
                            'willBeUpgradedAt': ud.will_be_upgraded_at if ud else None
                        }
                    }
                }
        vt = VillageTroops.objects.get(village=village)
        village_dict['troops'][
            'inVillage'] = vt.in_village_troops_quantity_json
        village_dict['troops']['total'] = vt.total_troops_quantity_json

        incoming_stranger_troops = TroopMovements.objects.filter(
            target_village=village)

        village_dict['troops']['incomingStrangerTroops'] = {}
        if incoming_stranger_troops:
            for ist in incoming_stranger_troops:
                village_dict['troops']['incomingStrangerTroops'][ist.task_id] = {
                    "from": ist.home_village_id,
                    "to": ist.target_village_id,
                    "movementType": ist.movement_type,
                    "arrivalTime": ist.arrival_time,
                }

        else:
            pass

        village_troops_movements = TroopMovements.objects.filter(
            home_village=village)

        village_dict['troops']['onMove'] = {}
        if village_troops_movements:
            for vtm in village_troops_movements:
                village_dict['troops']['onMove'][vtm.task_id] = {
                    "from": vtm.home_village_id,
                    "to": vtm.target_village_id,
                    "movementType": vtm.movement_type,
                    "state": vtm.state,
                    "arrivalTime": vtm.arrival_time,
                    "troops": vtm.moving_troops_json
                }

        village_dict['troops']['trainingQueue'] = {
            'infantry': [{
                'unit_name': training_element.unit_name,
                'units_left': training_element.units_left,
                'will_end_at': training_element.will_end_at
            } for training_element in village.training_queues.filter(unit_type="infantry").reverse()],
            'cavalry': [{
                'unit_name': training_element.unit_name,
                'units_left': training_element.units_left,
                'will_end_at': training_element.will_end_at
            } for training_element in village.training_queues.filter(unit_type="cavalry").reverse()],
            'siegeWeapons': [{
                'unit_name': training_element.unit_name,
                'units_left': training_element.units_left,
                'will_end_at': training_element.will_end_at
            } for training_element in village.training_queues.filter(unit_type="siegeWeapons").reverse()],
            'other': []
        }
        return village_dict

    def get_my_villages(self):

        villages_querysets = Villages.objects.filter(user_id=self.id)
        my_villages = []
        for village in villages_querysets:
            village_dict = self.get_my_village(village)

            # TODO get trainingQueue and fill dict above

            my_villages.append(village_dict)

        return my_villages

    def get_player_profile_dict(self):
        players_villages = [vil.get_village_profile_dict()
                            for vil in self.villages.all()]
        return {
            'clan': '',
            'points': self.points,
            'regionSelected': self.is_region_selected,
            'user_id': self.id,
            'playersVillages': players_villages,
            'username': self.username,
        }

    # TODO move this function to Villages
    def get_current_resources(self, village_id):
        currentResources = {}
        for resourceBuildingName, rb in gameConfig['buildings']['resources'].items():
            resource_building = VillageBuildings.objects.get(
                village_id=int(village_id), building_name=resourceBuildingName)
            rbd = ResourceBuildingDetails.objects.get(
                id=str(resource_building.resource_building_detail_id))
            now = datetime.datetime.now(pytz.utc)
            # village = self.getVillageById(village_id)
            resourceSum = rbd.sum
            resourceLevel = str(resource_building.level)
            resourceLastInteractionDate = rbd.last_interaction_date
            hourlyProductionByLevel = gameConfig['buildings']['resources'][
                resource_building.building_name]['hourlyProductionByLevel'][resourceLevel]
            totalHoursOfProduction = (
                now - resourceLastInteractionDate).total_seconds() / 60 / 60
            totalCurrentResource = (
                totalHoursOfProduction * hourlyProductionByLevel) + resourceSum
            storage_level = str(VillageBuildings.objects.get(
                village_id=village_id, building_name='storage').level)
            if totalCurrentResource >= gameConfig['buildings']['storage']['capacity'][storage_level]:
                totalCurrentResource = gameConfig['buildings'][
                    'storage']['capacity'][storage_level]
            currentResources[resourceBuildingName] = int(totalCurrentResource)
        return currentResources

    def set_upgrading_time_and_state(self, village_id, building_path, reqiured_time, task_id, now):
        user_id = self.id
        # village = db.collection('players').document(user_id).collection('villages').document(village_id)
        # now = datetime.datetime.now()
        # now = datetime.datetime.fromtimestamp(now)
        willEnd = now + datetime.timedelta(0, reqiured_time)
        if '.' in building_path:
            vb = VillageBuildings.objects.get(building_name=building_path.split('.')[
                                              1], village_id=village_id)
            ud = UpgradingDetails.objects.create(
                task_id=task_id,
                started_upgrading_at=now,
                will_be_upgraded_at=willEnd,
            )
            vb.upgrading_details_id = ud
        else:
            vb = VillageBuildings.objects.get(
                building_name=building_path, village_id=village_id)
            ud = UpgradingDetails.objects.create(
                task_id=task_id,
                started_upgrading_at=now,
                will_be_upgraded_at=willEnd,
            )
            vb.upgrading_details_id = ud
        vb.is_upgrading = True
        vb.save()
        # village.update({
        #     'buildings.'+building_path+'.upgrading.time.startedUpgradingAt' : now,
        #     'buildings.'+building_path+'.upgrading.time.willBeUpgradedAt' : willEnd,
        #     'buildings.'+building_path+'.upgrading.state' : True,
        #     'buildings.'+building_path+'.upgrading.task_id' : task_id
        # })

    def upgrade_building(self, village_id, building_path):
        if '.' in building_path:
            vb = VillageBuildings.objects.get(building_name=building_path.split('.')[
                                              1], village_id=village_id)
        else:
            vb = VillageBuildings.objects.get(
                building_name=building_path, village_id=village_id)
        vb.level += 1
        vb.is_upgrading = False
        ud = vb.upgrading_details_id
        ud.delete()
        vb.upgrading_details_id = None
        vb.save()

    def has_resources_to_train_units(self, village_id, unit_type, units_to_train):
        required_wood_sum, reqiured_iron_sum, reqiured_clay_sum = 0, 0, 0
        current_resources = self.get_current_resources(village_id)
        for unit in units_to_train:
            required_wood, reqiured_iron, reqiured_clay = get_required_resources_to_train_unit(
                unit_type,
                unit['unit_name'],
                unit['amount']
            )
            required_wood_sum += required_wood
            reqiured_iron_sum += reqiured_iron
            reqiured_clay_sum += reqiured_clay

        print(required_wood_sum, reqiured_iron_sum, reqiured_clay_sum)

        return (current_resources['woodCamp'] >= required_wood_sum
                and current_resources['ironMine'] >= reqiured_iron_sum
                and current_resources['clayPit'] >= reqiured_clay_sum)

    def get_reports(self):

        reports = Reports.objects.filter(sended_to_user=self)
        reports_arr = []
        for report in reports:
            report_dict = {
                'type': report.type,
                'date': report.created_at,
                'viewed': report.is_viewed,
                'content': report.content
            }
            reports_arr.append(report_dict)
        return reports_arr


class Villages(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    village_name = models.CharField(max_length=20)
    coords_x = models.IntegerField()
    coords_y = models.IntegerField()
    points = models.IntegerField(default=0)
    has_all_buildings = models.BooleanField(default=False)
    has_village_troops = models.BooleanField(default=False)

    # Relationship Fields
    region = models.ForeignKey(
        'wololo.Regions',
        on_delete=models.CASCADE, related_name="villagess",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="villages", blank=True, null=True
    )

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.village_name

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_villages_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_villages_update', args=(self.pk,))

    def _setup_village(self):
        pass

    def train_unit(self, unit_type, unit_name):
        # TODO check if population limit is not reached

        self.village_troops.in_village_troops_quantity_json[
            unit_type][unit_name] += 1
        self.village_troops.save()

        tq = self._get_training_queue_or_queues(unit_type, unit_name)

        if tq[0].units_left is 0 or tq[0].units_left is 1:
            TrainingQueue.objects.get(id=tq[0].id).delete()
        else:
            tq = TrainingQueue.objects.get(id=tq[0].id)
            tq.units_left -= 1
            tq.save()

    def get_last_training_queue_by_unit_type(self, unit_type):
        tq = self.training_queues.filter(unit_type=unit_type)
        # return last added element if exists
        return False if len(tq.all()) == 0 else tq.all()[0]

    def add_to_training_queue(self, chain_id, unit_type, unit_name,
                              number_of_units_to_train, will_start_at, will_end_at):
        return TrainingQueue.objects.create(
            village=self,
            chain_id=chain_id,
            unit_type=unit_type,
            unit_name=unit_name,
            units_left=number_of_units_to_train,
            started_at=will_start_at,
            will_end_at=will_end_at
        )

    def get_required_time_for_train_units(self, unit_type, unit_name):

        reqiured_time = gameConfig['units'][unit_type][
            unit_name]['neededTrainingBaseTime']
        # TODO get building_name dynamically from unit_type
        building_level = self.village_buildings.get(
            building_name='barracks').level
        speed_percantage_of_barracks = \
            gameConfig['buildings']['barracks']['trainingSpeed'][str(
                building_level)]
        reqiured_time = int(reqiured_time - (reqiured_time *
                                             speed_percantage_of_barracks / 100)) * 60  # seconds

        return reqiured_time

    def get_units_left(self, unit_type, unit_name):
        tq = self._get_training_queue_or_queues(unit_type, unit_name)
        print(tq)
        units_left = tq[0].units_left
        return units_left

    def _get_training_queue_or_queues(self, unit_type, unit_name):
        return self.training_queues.filter(unit_type=unit_type, unit_name=unit_name)

    def get_village_profile_dict(self):
        return {
            'village_id': self.id,
            'villageName': self.village_name,
            'points': self.points,
            'user_id': self.user.id,
            'playerName': self.user.username,
            'clan': '',
            'region': self.region.name,
            'coords': {
                'x': self.coords_x,
                'y': self.coords_y
            }
        }


class Regions(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_regions_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_regions_update', args=(self.pk,))


class VillageTroops(models.Model):

    # Fields
    in_village_troops_quantity_json = JSONField(
        default=default_fresh_troops_dict)
    on_move_troops_quantity_json = JSONField(default=default_fresh_troops_dict)

    @property
    def total_troops_quantity_json(self):
        total_troops_quantity_json = {}
        for unit_type_name, unit_type in self.in_village_troops_quantity_json.items():
            total_troops_quantity_json[unit_type_name] = {}
            for unit_name, in_village_unit_amount in unit_type.items():
                total_troops_quantity_json[unit_type_name][unit_name] = \
                    in_village_unit_amount + \
                    self.on_move_troops_quantity_json[
                        unit_type_name][unit_name]
        return total_troops_quantity_json
    # Relationship Fields
    village = models.OneToOneField(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="village_troops",
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_villagetroops_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_villagetroops_update', args=(self.pk,))


class TrainingQueue(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    chain_id = models.TextField(max_length=100)
    unit_name = models.CharField(max_length=30)
    unit_type = models.CharField(max_length=30)
    units_left = models.PositiveIntegerField()
    started_at = models.DateTimeField()
    will_end_at = models.DateTimeField()

    # Relationship Fields
    village = models.ForeignKey(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="training_queues",
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_trainingqueue_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_trainingqueue_update', args=(self.pk,))


class Reports(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    type = models.CharField(
        max_length=15,
        choices=[
            ('battle', 'Battle')
        ]
    )
    is_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    # Relationship Fields
    sended_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="reports",
    )

    @property
    def content(self):
        if self.type == 'battle':
            br = BattleReports.objects.get(report=self)
            br_dict = {
                'attacker': {
                    'user_id': br.attacker.id,
                    'username': br.attacker.username,
                    'villageName': br.attacker_village.village_name,
                    'village_id': br.attacker_village.id,
                    'result': br.attacker_battle_result.result,
                    'units_result': br.attacker_battle_result.
                    quantity_and_losses_troops_json
                },
                'defender': {
                    'user_id': br.defender.id,
                    'username': br.defender.username,
                    'villageName': br.defender_village.village_name,
                    'village_id': br.defender_village.id,
                    'result': br.defender_battle_result.result,
                    'units_result': br.defender_battle_result.
                    quantity_and_losses_troops_json
                }
            }
            return br_dict

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_reports_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_reports_update', args=(self.pk,))


class BattleResults(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    quantity_and_losses_troops_json = JSONField(default=dict)
    result = models.CharField(
        max_length=5,
        choices=[
            ('won', 'Won'),
            ('draw', 'Draw'),
            ('lost', 'Lost')
        ]
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_battleresults_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_battleresults_update', args=(self.pk,))


class BattleReports(models.Model):

    # Fields
    is_details_hidden = models.BooleanField(default=False)

    # Relationship Fields
    report = models.OneToOneField(
        'wololo.Reports',
        on_delete=models.CASCADE
    )
    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="battlereport",
    )
    attacker_village = models.ForeignKey(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="attack_br",
    )
    attacker_battle_result = models.ForeignKey(
        'wololo.BattleResults',
        on_delete=models.CASCADE, related_name="battlereportss",
    )
    defender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="battlereportss_2",
    )
    defender_village = models.ForeignKey(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="defend_br",
    )
    defender_battle_result = models.ForeignKey(
        'wololo.BattleResults',
        on_delete=models.CASCADE, related_name="battlereportss_2",
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_battlereports_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_battlereports_update', args=(self.pk,))


class TroopMovements(models.Model):

    # Fields
    task_id = models.TextField(max_length=100)
    arrival_time = models.DateTimeField()  # TODO calculate this on save() method
    movement_duration_seconds = models.PositiveIntegerField()
    moving_troops_json = JSONField(default=dict)
    movement_type = models.CharField(max_length=9)  # attack/support
    state = models.CharField(max_length=9)  # going/returning

    # Relationship Fields
    home_village = models.ForeignKey(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="troopmovementss",
    )
    target_village = models.ForeignKey(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="troopmovementss_2",
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_troopmovements_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_troopmovements_update', args=(self.pk,))


class VillageBuildings(models.Model):

    # Fields
    building_name = models.CharField(max_length=30)
    is_upgrading = models.BooleanField(default=False)
    is_resource_building = models.BooleanField(default=False)
    level = models.PositiveIntegerField(default=0)

    # Relationship Fields
    village = models.ForeignKey(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="village_buildings",
    )
    upgrading_details_id = models.OneToOneField(
        'wololo.UpgradingDetails',
        on_delete=models.CASCADE, related_name="village_building", blank=True, null=True
    )
    resource_building_detail_id = models.OneToOneField(
        'wololo.ResourceBuildingDetails',
        on_delete=models.CASCADE, related_name="village_building", blank=True, null=True
    )

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_villagebuildings_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_villagebuildings_update', args=(self.pk,))


class UpgradingDetails(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=100)
    started_upgrading_at = models.DateTimeField()
    will_be_upgraded_at = models.DateTimeField()

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_upgradingdetails_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_upgradingdetails_update', args=(self.pk,))


class ResourceBuildingDetails(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    last_interaction_date = models.DateTimeField(auto_now_add=True)
    sum = models.IntegerField(default=0)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_resourcebuildingdetails_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('wololo_resourcebuildingdetails_update', args=(self.pk,))


def get_required_resources_to_train_unit(unit_type, unit_name, number_of_units_to_train):
    reqiured_wood = gameConfig['units'][unit_type][unit_name]['Cost']['Wood'] * \
        number_of_units_to_train
    reqiured_iron = gameConfig['units'][unit_type][unit_name]['Cost']['Iron'] * \
        number_of_units_to_train
    reqiured_clay = gameConfig['units'][unit_type][unit_name]['Cost']['Clay'] * \
        number_of_units_to_train

    return reqiured_wood, reqiured_iron, reqiured_clay


def get_public_villages(current_user_id=None):

    public_villages = Villages.objects.exclude(user_id=None)
    public_villages_info = []

    for village in public_villages:
        village_dict = {}
        village_dict['user_id'] = village.user_id
        village_dict['village_id'] = village.id
        if(village_dict['user_id'] == current_user_id):
            village_dict['owner'] = True
        village_dict['coords'] = {
            'x': village.coords_x,
            'y': village.coords_y
        }
        village_dict['villageName'] = village.village_name
        village_dict['playerName'] = str(village.user)
        village_dict['points'] = village.points

        public_villages_info.append(village_dict)

    return public_villages_info
