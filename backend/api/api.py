from wololo import models
from . import serializers
from rest_framework import viewsets, permissions


class VillagesViewSet(viewsets.ModelViewSet):
    """ViewSet for the Villages class"""

    queryset = models.Villages.objects.all()
    serializer_class = serializers.VillagesSerializer
    #permission_classes = [permissions.IsAuthenticated]


class RegionsViewSet(viewsets.ModelViewSet):
    """ViewSet for the Regions class"""

    queryset = models.Regions.objects.all()
    serializer_class = serializers.RegionsSerializer
    #permission_classes = [permissions.IsAuthenticated]


class VillageTroopsViewSet(viewsets.ModelViewSet):
    """ViewSet for the VillageTroops class"""

    queryset = models.VillageTroops.objects.all()
    serializer_class = serializers.VillageTroopsSerializer
    #permission_classes = [permissions.IsAuthenticated]


class TrainingQueueViewSet(viewsets.ModelViewSet):
    """ViewSet for the TrainingQueue class"""

    queryset = models.TrainingQueue.objects.all()
    serializer_class = serializers.TrainingQueueSerializer
    #permission_classes = [permissions.IsAuthenticated]


class ReportsViewSet(viewsets.ModelViewSet):
    """ViewSet for the Reports class"""

    queryset = models.Reports.objects.all()
    serializer_class = serializers.ReportsSerializer
    #permission_classes = [permissions.IsAuthenticated]


class BattleResultsViewSet(viewsets.ModelViewSet):
    """ViewSet for the BattleResults class"""

    queryset = models.BattleResults.objects.all()
    serializer_class = serializers.BattleResultsSerializer
    #permission_classes = [permissions.IsAuthenticated]


class BattleReportsViewSet(viewsets.ModelViewSet):
    """ViewSet for the BattleReports class"""

    queryset = models.BattleReports.objects.all()
    serializer_class = serializers.BattleReportsSerializer
    #permission_classes = [permissions.IsAuthenticated]


class TroopMovementsViewSet(viewsets.ModelViewSet):
    """ViewSet for the TroopMovements class"""

    queryset = models.TroopMovements.objects.all()
    serializer_class = serializers.TroopMovementsSerializer
    #permission_classes = [permissions.IsAuthenticated]


class VillageBuildingsViewSet(viewsets.ModelViewSet):
    """ViewSet for the VillageBuildings class"""

    queryset = models.VillageBuildings.objects.all()
    serializer_class = serializers.VillageBuildingsSerializer
    #permission_classes = [permissions.IsAuthenticated]


class UpgradingDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for the UpgradingDetails class"""

    queryset = models.UpgradingDetails.objects.all()
    serializer_class = serializers.UpgradingDetailsSerializer
    #permission_classes = [permissions.IsAuthenticated]


class ResourceBuildingDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for the ResourceBuildingDetails class"""

    queryset = models.ResourceBuildingDetails.objects.all()
    serializer_class = serializers.ResourceBuildingDetailsSerializer
    #permission_classes = [permissions.IsAuthenticated]