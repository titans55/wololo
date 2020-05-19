import { Routes, RouterModule } from "@angular/router";
import { MapComponent } from "./component/map/component/map.component";
import { VillageComponent } from "./component/village/component/village.component";
import { AfterRouterOutletEnum } from "./enum/after-router-outlet.enum";
import { AfterLoginComponent } from "./component/after-login.component";
import { AuthGuard } from "./service/user/guard/auth.guard";
import { BarracksComponent } from "./component/buildings/barracks/component/barracks.component";

export enum AfterLoginRoutesEnum {
  MAP = "map",
  VILLAGE = "village",
  BARRACKS = "barracks",
}

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
    ],
  },
];

export const AfterLoginRoute = RouterModule.forChild(AfterLoginRoutes);
