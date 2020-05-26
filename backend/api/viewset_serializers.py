from wololo import models

from rest_framework import serializers


class VillagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Villages
        fields = (
            'pk', 
            'id', 
            'village_name', 
            'coords_x', 
            'coords_y', 
            'points', 
            'has_all_buildings', 
            'has_village_troops', 
        )


class RegionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Regions
        fields = (
            'pk', 
            'id', 
            'name', 
        )


class VillageTroopsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VillageTroops
        fields = (
            'pk', 
            'on_move_troops_quantity_json', 
        )


class TrainingQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TrainingQueue
        fields = (
            'pk', 
            'id', 
            'chain_id', 
            'unit_name', 
            'unit_type', 
            'units_left', 
            'started_at', 
            'will_end_at', 
        )


class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Reports
        fields = (
            'id', 
            'type', 
            'is_viewed', 
            'created_at',
            'content' 
        )


class BattleResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BattleResults
        fields = (
            'pk', 
            'id', 
            'quantity_and_losses_troops_json', 
            'result', 
        )


class BattleReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BattleReports
        fields = (
            'pk', 
            'is_details_hidden', 
        )


class TroopMovementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TroopMovements
        fields = (
            'pk', 
            'task_id', 
            'movement_duration_seconds', 
            'moving_troops_json', 
            'movement_type', 
        )


class VillageBuildingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VillageBuildings
        fields = (
            'pk', 
            'building_name', 
            'is_upgrading', 
            'is_resource_building', 
            'level', 
        )


class UpgradingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UpgradingDetails
        fields = (
            'pk', 
            'id', 
            'task_id', 
            'started_upgrading_at', 
            'will_be_upgraded_at', 
        )


class ResourceBuildingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResourceBuildingDetails
        fields = (
            'pk', 
            'id', 
            'last_interaction_date', 
            'sum', 
        )
