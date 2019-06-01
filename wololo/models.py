from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
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

    def get_my_villages(self):

        villages_querysets = Villages.objects.filter(user_id=self.id)
        my_villages = []
        for village in villages_querysets:
            village_dict = {
                'buildings' : {
                    'resources' : {}
                },
                'villageName' : village.village_name,
                'troops' : {}
            }
            village_building_querysets = VillageBuildings.objects.filter(village_id = village)
            for village_building in village_building_querysets:
                if village_building.is_resource_building:
                    rbd = village_building.resource_building_detail_id
                    ud = village_building.upgrading_details_id
                    print(rbd, ud)
                    village_dict['buildings']['resources'][village_building.building_name] = {
                        'level' : village_building.level,
                        'sum' : rbd.sum,
                        'lastInteractionDate' : rbd.last_interaction_date,
                        'upgrading' : {
                            'state' : village_building.is_upgrading,
                            'task_id' : ud.task_id if ud else '',
                            'time' : {
                                'startedUpgradingAt' : ud.started_upgrading_at if ud else '',
                                'willBeUpgradedAt' : ud.will_be_upgraded_at if ud else ''
                            }
                        }
                    }
                else:
                    ud = village_building.upgrading_details_id
                    village_dict['buildings'][village_building.building_name] = {
                        'level' : village_building.level,
                        'upgrading' : {
                            'state' : village_building.is_upgrading,
                            'task_id' : ud.task_id if ud else '',
                            'time' : {
                                'startedUpgradingAt' : ud.started_upgrading_at if ud else '',
                                'willBeUpgradedAt' : ud.will_be_upgraded_at if ud else ''
                            }
                        }
                    }
            vt = VillageTroops.objects.get(village_id = village)
            village_dict['troops']['inVillage'] = vt.in_village_troops_quantity_json
            village_dict['troops']['total'] = vt.total_troops_quantity_json
            
            incoming_stranger_troops = TroopMovements.objects.filter(target_village_id = village)
            if incoming_stranger_troops:
                for ist in incoming_stranger_troops:
                    village_dict['troops']['incomingStrangerTroops'][ist.task_id] = {
                        "from" : ist.home_village_id,
                        "to" : ist.target_village_id,
                        "movementType" : ist.movement_type,
                        "arrivalTime" : ist.arrival_time,
                    }
                    
            else:
                village_dict['troops']['incomingStrangerTroops'] = {}

            village_troops_movements = TroopMovements.objects.filter(home_village_id = village)
            if village_troops_movements:
                for vtm in village_troops_movements:
                    village_dict['troops']['incomingStrangerTroops'][vtm.task_id] = {
                        "from" : vtm.home_village_id,
                        "to" : vtm.target_village_id,
                        "movementType" : vtm.movement_type,
                        "state" : vtm.state,
                        "arrivalTime" : vtm.arrival_time,
                        "troops" : vtm.moving_troops_json
                    }
                    
            else:
                village_dict['troops']['onMove']  = {}       

            for buildingName, building in village_dict['buildings'].items():
                if buildingName == 'resources': 
                    for resource in building:
                        village_dict['buildings']['resources'][resource]['upgrading']['state'] = 'true' if village_dict['buildings']['resources'][resource]['upgrading']['state'] else 'false'
                else :
                    village_dict['buildings'][buildingName]['upgrading']['state'] = 'true' if village_dict['buildings'][buildingName]['upgrading']['state'] else 'false'

            village_dict['troops']['trainingQueue'] = {
                'infantry' : [],
                'cavalry' : [],
                'siegeWeapons' : [],
                'other' : []
            }

            #get trainingQueue and fill dict above 
            pass

            my_villages.append(village_dict)
        
        return my_villages

    def get_reports(self):
        reports = []
        return reports

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
        on_delete=models.CASCADE, related_name="villagess", blank=True, null=True
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


class Regions(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=30)


    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.region_name

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('wololo_regions_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('wololo_regions_update', args=(self.pk,))


class VillageTroops(models.Model):

    

    # Fields
    in_village_troops_quantity_json = JSONField(default=default_fresh_troops_dict)
    on_move_troops_quantity_json = JSONField(default= default_fresh_troops_dict)
    total_troops_quantity_json = JSONField(default=default_fresh_troops_dict)

    # Relationship Fields
    village_id = models.OneToOneField(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="villagetroopss", 
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
    chain_id = models.TextField(max_length=100)
    unit_name = models.CharField(max_length=30)
    unit_type = models.CharField(max_length=30)
    units_left = models.PositiveIntegerField()
    started_at = models.DateTimeField()
    will_end_at = models.DateTimeField()

    # Relationship Fields
    village = models.ForeignKey(
        'wololo.Villages',
        on_delete=models.CASCADE, related_name="trainingqueues", 
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
    type = models.CharField(max_length=15)
    is_viewed = models.BooleanField(default=False)

    # Relationship Fields
    sended_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="reportss", 
    )

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
    report_id = models.OneToOneField(
        'wololo.Reports',
        on_delete=models.CASCADE, related_name="battlereportss", 
    )
    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="battlereportss", 
    )
    attacker_battle_result_id = models.OneToOneField(
        'wololo.BattleResults',
        on_delete=models.CASCADE, related_name="battlereportss", 
    )
    defender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="battlereportss_2", 
    )
    defender_battle_result_id = models.OneToOneField(
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
    arrival_time = models.DateTimeField()
    moving_troops_json = JSONField(default=dict)
    movement_type = models.CharField(max_length=9) #attack/support
    state = models.CharField(max_length=9) #going/returning

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
        on_delete=models.CASCADE, related_name="villagebuildingss", 
    )
    upgrading_details_id = models.OneToOneField(
        'wololo.UpgradingDetails',
        on_delete=models.CASCADE, related_name="villagebuildingss", blank=True, null=True
    )
    resource_building_detail_id = models.OneToOneField(
        'wololo.ResourceBuildingDetails',
        on_delete=models.CASCADE, related_name="villagebuildingss", blank=True, null=True
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
    task_id = models.CharField(max_length=30)
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

