from django.urls import path, include
from rest_framework import routers

from . import api
from api.views.after_login.villages_view import VillagesView
from api.views.after_login.map_view import MapView

router = routers.DefaultRouter()
router.register(r'villages', api.VillagesViewSet)
router.register(r'regions', api.RegionsViewSet)
router.register(r'villagetroops', api.VillageTroopsViewSet)
router.register(r'trainingqueue', api.TrainingQueueViewSet)
router.register(r'reports', api.ReportsViewSet)
router.register(r'battleresults', api.BattleResultsViewSet)
router.register(r'battlereports', api.BattleReportsViewSet)
router.register(r'troopmovements', api.TroopMovementsViewSet)
router.register(r'villagebuildings', api.VillageBuildingsViewSet)
router.register(r'upgradingdetails', api.UpgradingDetailsViewSet)
router.register(r'resourcebuildingdetails', api.ResourceBuildingDetailsViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('v1/', include(router.urls)),
    path('villagesView/<int:village_index>', VillagesView.as_view(), name='villageApi'),
    path('mapView/', MapView.as_view()),
)
