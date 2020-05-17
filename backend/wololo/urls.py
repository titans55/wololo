from django.urls import path

# from . import views
from wololo.views.afterLogin.buildings import barracksView
from wololo.views.afterLogin import mapView, villagesView, clansView, reportsView, rankingView, commandCenterView
from wololo.views.beforeLogin import selectingRegionView, landingView
from wololo.views.afterLogin.profiles import playerProfileView, villageProfileView
from wololo.views import auth
from wololo.views.beforeLogin.registerView import RegisterView


urlpatterns = [
    path('', landingView.landingPage, name='landingPage'),
    path('register', RegisterView.as_view(), name='register'),
    path('create_account', auth.create_account,
         name='create_account'),  # FORM CALL
    path('game/selectRegion',
         selectingRegionView.selectRegionOnFirstLoginView, name='selectRegion'),


    path('game', villagesView.villages, name='myVillage'),
    path('game/<int:village_index>', villagesView.villages),

    path('game/map', mapView.map, name='map'),
    path('game/<int:village_index>/map', mapView.map),
    path('game/map/findPath', mapView.find_path),  # AJAX CALL

    path('game/barracks', barracksView.barracks, name='barracks'),
    path('game/<int:village_index>/barracks',
         barracksView.barracks, name='barracks'),
    path('game/barracks/trainUnits', barracksView.trainUnits,
         name='trainUnits'),  # AJAX CALL

    path('game/clans', clansView.clans, name='clans'),
    path('game/<int:village_index>/clans', clansView.clans),

    path('game/reports', reportsView.reportsList, name='reportsList'),
    path('game/<int:village_index>/reports', reportsView.reportsList),
    path('game/reports/<int:report_index>', reportsView.report, name='report'),
    path('game/<int:village_index>/reports/<int:report_index>', reportsView.report),

    path('game/ranking', rankingView.ranking, name='ranking'),
    path('game/<int:village_index>/ranking', rankingView.ranking),

    path('game/players/<str:player_id>',
         playerProfileView.playerProfile, name='playerProfile'),
    path('game/<int:village_index>/players/<str:player_id>',
         playerProfileView.playerProfile),

    path('game/villages/<str:village_id>',
         villageProfileView.villageProfile, name='villageProfile'),
    path('game/<int:village_index>/villages/<str:village_id>',
         villageProfileView.villageProfile),

    path('game/commandCenter', commandCenterView.commandCenter,
         name='commandCenter'),  # FORM CALL AND NORMAL VIEW
    path('game/<int:village_index>/commandCenter',
         commandCenterView.commandCenter),
    path('game/commandCenter/attack', commandCenterView.sendAttack),  # FORM CALL

    # AJAX CALL
    path('game/upgrade', villagesView.upgrade, name='upgrade'),
    path('game/cancelUpgrade', villagesView.cancelUpgrade, name='cancelUpgrade'),

    # FORM CALL
    path('game/selectingRegion', selectingRegionView.selectingRegion),
    path('verifyLogin', auth.verifyLogin, name='verifyLogin'),
    path('logout', auth.logout, name='verifyLogin'),


]
