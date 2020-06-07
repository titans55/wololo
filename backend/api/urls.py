from django.urls import path, include
from rest_framework import routers

from . import api
from api.views.after_login.villages_view import VillagesView, UpgradeBuildingView
from api.views.after_login.map_view import MapView
from api.views.after_login.buildings.unit_training_buildings.barracks_view import BarracksView
from api.views.after_login.reports_view import ReportsList, ReportViewed
from api.views.after_login.ranking_view import Ranking
from api.views.after_login.profiles.player_profile_view import PlayerProfile
from api.views.after_login.profiles.village_profile_view import VillageProfile
from api.views.after_login.command_center.command_center_view import \
    AttackView, CalculateDistanceBetweenTwoVillages

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
    path('villagesView/<int:village_index>',
         VillagesView.as_view(), name='villageApi'),
    path('upgrade-building/<int:village_index>', UpgradeBuildingView.as_view()),
    path('barracks/train-units', BarracksView.as_view()),
    path('mapView/', MapView.as_view()),
    path('reports/', ReportsList.as_view()),
    path('report-viewed/<int:report_id>', ReportViewed.as_view()),
    path('ranking/', Ranking.as_view()),
    path('player-profile/<str:username>', PlayerProfile.as_view()),
    path('village-profile/<int:village_id>', VillageProfile.as_view()),
    path('command-center/calculate-distance',
         CalculateDistanceBetweenTwoVillages.as_view()),
    path('command-center/attack', AttackView.as_view()),
)
