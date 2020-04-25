import { Routes, RouterModule } from "@angular/router";
import { MapComponent } from "./component/map/component/map.component";
import { VillageComponent } from "./component/village/component/village.component";

export enum AfterLoginRoutesEnum {
  MAP = "map",
  VILLAGE = "village",
}

export const AfterLoginRoutes: Routes = [
  {
    path: AfterLoginRoutesEnum.MAP,
    component: MapComponent,
  },
  {
    path: AfterLoginRoutesEnum.VILLAGE,
    component: VillageComponent,
  },
];

export const AfterLoginRoute = RouterModule.forChild(AfterLoginRoutes);
