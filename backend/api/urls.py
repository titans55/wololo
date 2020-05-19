from django.urls import path, include
from rest_framework import routers

from . import api
from api.views.after_login.villages_view import VillagesView, UpgradeBuildingView
from api.views.after_login.map_view import MapView
from api.views.after_login.buildings.barracks_view import TrainInfantryView

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

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
    path('token-auth/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('villagesView/<int:village_index>', VillagesView.as_view(), name='villageApi'),
    path('upgrade-building/<int:village_index>', UpgradeBuildingView.as_view()),
    path('barracks/train-units', TrainInfantryView.as_view()),
    path('mapView/', MapView.as_view()),
)
