import { Routes, RouterModule } from "@angular/router";
import { MapComponent } from "./component/map/component/map.component";
import { VillageComponent } from "./component/village/component/village.component";
import { AfterRouterOutletEnum } from "./enum/after-router-outlet.enum";
import { AfterLoginComponent } from "./component/after-login.component";
import { AuthGuard } from "./service/user/guard/auth.guard";

export enum AfterLoginRoutesEnum {
  MAP = "map",
  VILLAGE = "village",
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
    ],
  },
];

export const AfterLoginRoute = RouterModule.forChild(AfterLoginRoutes);
