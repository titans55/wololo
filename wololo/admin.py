from django.contrib import admin
from django import forms
from .models import Users, Villages, Regions, VillageTroops, TrainingQueue, Reports, BattleResults, BattleReports, TroopMovements, VillageBuildings, UpgradingDetails, ResourceBuildingDetails

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from wololo.commonFunctions import getGameConfig, getFreshBuildingLevel, getFreshVillagePoints

game_config = getGameConfig()

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Users
        fields = '__all__'


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    list_display = ['id', 'points', 'username', 'number_of_villages', 'email', 'is_region_selected', 'is_unviewed_reports_exists', 'clan_id',]

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('is_region_selected','is_unviewed_reports_exists','number_of_villages', 'points')}),
    )


admin.site.register(Users, MyUserAdmin)


class VillagesAdminForm(forms.ModelForm):

    class Meta:
        model = Villages
        fields = '__all__'


class VillagesAdmin(admin.ModelAdmin):
    form = VillagesAdminForm
    list_display = ['id', 'village_name',
        'user', 'has_all_buildings',
        'has_village_troops', 'coords_x',
        'coords_y', 'points', 'region'
    ]
    readonly_fields = ['id']

    actions = ['create_village_buildings_and_troops']

    def create_village_buildings_and_troops(self, request, queryset):

        for village in queryset:
            if(village.has_all_buildings):
                self.message_user(request, "%s has buildings already." % village)
            else:
                village.points = getFreshVillagePoints()
                for buildingName, building in game_config['buildings'].items():
                    if buildingName == 'resources' :
                        for resourceBuildingName, resourceBuilding in building.items():
                            vbExists = VillageBuildings.objects.filter(village_id = village.id, building_name = resourceBuildingName)
                            if vbExists:
                                vbExists = vbExists.get()
                                rbdExists = ResourceBuildingDetails.objects.filter(id = str(vbExists.resource_building_detail_id))#check if exists
                                self.message_user(request, str(vbExists.building_name) + " VillageBuildings already exists.")
                                if(rbdExists):
                                    self.message_user(request, str(rbdExists) + " ResourceBuildingDetails already exists.")
                            
                            if not vbExists:
                                rbd = ResourceBuildingDetails.objects.create()
                                VillageBuildings.objects.create(
                                    building_name = resourceBuildingName, 
                                    is_resource_building = True,
                                    resource_building_detail_id = rbd,
                                    village = village,
                                    level = getFreshBuildingLevel(resourceBuildingName)
                                )
                    else:
                        vbExists = VillageBuildings.objects.filter(village_id = village.id, building_name = buildingName)#check if exists
                        if not vbExists:
                            VillageBuildings.objects.create(
                                building_name = buildingName, 
                                village = village,
                                level = getFreshBuildingLevel(buildingName)
                            )
                        else:
                            self.message_user(request, str(vbExists.get().building_name) + " VillageBuildings already exists.")

            VillageTroops.objects.create(village_id = village)

            village.has_all_buildings = True
            village.has_village_troops = True
            village.save()

       
admin.site.register(Villages, VillagesAdmin)


class RegionsAdminForm(forms.ModelForm):

    class Meta:
        model = Regions
        fields = '__all__'


class RegionsAdmin(admin.ModelAdmin):
    form = RegionsAdminForm
    list_display = ['id', 'name']
    readonly_fields = ['id']

admin.site.register(Regions, RegionsAdmin)


class VillageTroopsAdminForm(forms.ModelForm):

    class Meta:
        model = VillageTroops
        fields = '__all__'


class VillageTroopsAdmin(admin.ModelAdmin):
    form = VillageTroopsAdminForm
    list_display = ['in_village_troops_quantity_json', 'on_move_troops_quantity_json', 'total_troops_quantity_json']
    # readonly_fields = ['in_village_troops_quantity', 'on_move_troops_quantity', 'total_troops_quantity']

admin.site.register(VillageTroops, VillageTroopsAdmin)



class TrainingQueueAdminForm(forms.ModelForm):

    class Meta:
        model = TrainingQueue
        fields = '__all__'


class TrainingQueueAdmin(admin.ModelAdmin):
    form = TrainingQueueAdminForm
    list_display = ['chain_id', 'unit_name', 'unit_type', 'units_left', 'started_at', 'will_end_at']
    # readonly_fields = ['chain_id', 'unit_name', 'unit_type', 'units_left', 'started_at', 'will_end_at']

admin.site.register(TrainingQueue, TrainingQueueAdmin)


class ReportsAdminForm(forms.ModelForm):

    class Meta:
        model = Reports
        fields = '__all__'


class ReportsAdmin(admin.ModelAdmin):
    form = ReportsAdminForm
    list_display = ['id', 'type', 'is_viewed', 'created_at', 'sended_to_user', 'content']
    readonly_fields = ['id']

admin.site.register(Reports, ReportsAdmin)


class BattleResultsAdminForm(forms.ModelForm):

    class Meta:
        model = BattleResults
        fields = '__all__'


class BattleResultsAdmin(admin.ModelAdmin):
    form = BattleResultsAdminForm
    list_display = ['id', 'quantity_and_losses_troops_json']
    readonly_fields = ['id']

admin.site.register(BattleResults, BattleResultsAdmin)


class BattleReportsAdminForm(forms.ModelForm):

    class Meta:
        model = BattleReports
        fields = '__all__'


class BattleReportsAdmin(admin.ModelAdmin):
    form = BattleReportsAdminForm
    list_display = ['report', 'attacker', 'attacker_battle_result',
        'defender', 'defender_battle_result']


admin.site.register(BattleReports, BattleReportsAdmin)


class TroopMovementsAdminForm(forms.ModelForm):

    class Meta:
        model = TroopMovements
        fields = '__all__'


class TroopMovementsAdmin(admin.ModelAdmin):
    form = TroopMovementsAdminForm
    list_display = ['task_id', 'movement_type', 'state', 'arrival_time', 'moving_troops_json']
    # readonly_fields = ['task_id', 'arrival_time', 'moving_troops_json']

admin.site.register(TroopMovements, TroopMovementsAdmin)


class VillageBuildingsAdminForm(forms.ModelForm):

    class Meta:
        model = VillageBuildings
        fields = '__all__'


class VillageBuildingsAdmin(admin.ModelAdmin):
    form = VillageBuildingsAdminForm
    list_display = ['building_name', 'village_id', 'level', 'is_upgrading', 'upgrading_details_id', 'is_resource_building', 'resource_building_detail_id']
    # readonly_fields = ['building_name', 'is_upgrading', 'is_resource_building']

admin.site.register(VillageBuildings, VillageBuildingsAdmin)


class UpgradingDetailsAdminForm(forms.ModelForm):

    class Meta:
        model = UpgradingDetails
        fields = '__all__'


class UpgradingDetailsAdmin(admin.ModelAdmin):
    form = UpgradingDetailsAdminForm
    list_display = ['id', 'task_id', 'started_upgrading_at', 'will_be_upgraded_at']
    readonly_fields = ['id']

admin.site.register(UpgradingDetails, UpgradingDetailsAdmin)


class ResourceBuildingDetailsAdminForm(forms.ModelForm):

    class Meta:
        model = ResourceBuildingDetails
        fields = '__all__'


class ResourceBuildingDetailsAdmin(admin.ModelAdmin):
    form = ResourceBuildingDetailsAdminForm
    list_display = ['id', 'last_interaction_date', 'sum']
    readonly_fields = ['id']

admin.site.register(ResourceBuildingDetails, ResourceBuildingDetailsAdmin)


