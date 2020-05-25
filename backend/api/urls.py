from django.urls import path, include
from rest_framework import routers

from . import api
from api.views.after_login.villages_view import VillagesView, UpgradeBuildingView
from api.views.after_login.map_view import MapView
from api.views.after_login.buildings.unit_training_buildings.barracks_view import BarracksView
from api.views.after_login.reports_view import reportsList, report
from api.views.after_login.ranking_view import ranking
from api.views.after_login.profiles.playerProfile_view import playerProfile
from api.views.after_login.profiles.villageProfile_view import villageProfile

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
    path('reports/', reportsList.as_view()),
    path('reports/<int:report_index>', report.as_view()),
    path('rank', ranking.as_view()),
    path('profile/<int:player_id>', playerProfile.as_view()),
    path('village/<int:village_id>', villageProfile.as_view()),
)
