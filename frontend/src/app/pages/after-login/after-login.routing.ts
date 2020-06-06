import { Routes, RouterModule } from "@angular/router";
import { MapComponent } from "./component/map/component/map.component";
import { VillageComponent } from "./component/village/component/village.component";
import { AfterLoginRoutesEnum } from "./enum/after-login-routes.enum";
import { AfterLoginComponent } from "./component/after-login.component";
import { AuthGuard } from "./service/user/guard/auth.guard";
import { BarracksComponent } from "./component/buildings/barracks/component/barracks.component";
import { RankingComponent } from "./component/ranking/component/ranking.component";
import { ReportsRoutes } from "./component/reports/reports.routing";
import { PlayerProfileComponent } from "./component/profile/component/player-profile/component/player-profile.component";
import { PlayerProfileRoutesEnum } from "./component/profile/component/player-profile/enum/player-profile-routes.enum";
import { VillageProfileComponent } from "./component/profile/component/village-profile/component/village-profile.component";
import { VillageProfileRoutesEnum } from "./component/profile/component/village-profile/enum/village-profile-routes.enum";

export const AfterLoginRoutes: Routes = [
  {
    path: "",
    component: AfterLoginComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: "",
        component: VillageComponent,
      },
      {
        path: AfterLoginRoutesEnum.MAP,
        component: MapComponent,
      },
      {
        path: AfterLoginRoutesEnum.BARRACKS,
        component: BarracksComponent,
      },
      {
        path: AfterLoginRoutesEnum.PLAYER_RANKING,
        component: RankingComponent,
      },
      {
        path: AfterLoginRoutesEnum.REPORTS,
        children: ReportsRoutes,
      },
      {
        path:
          AfterLoginRoutesEnum.PLAYER_PROFILE +
          "/:" +
          PlayerProfileRoutesEnum.USERNAME_URL_PARAM,
        component: PlayerProfileComponent,
      },
      {
        path:
          AfterLoginRoutesEnum.VILLAGE_PROFILE +
          "/:" +
          VillageProfileRoutesEnum.VILLAGE_ID_URL_PARAM,
        component: VillageProfileComponent,
      },
    ],
  },
];

export const AfterLoginRoute = RouterModule.forChild(AfterLoginRoutes);
