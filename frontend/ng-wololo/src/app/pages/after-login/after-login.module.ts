import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AfterLoginComponent } from "./component/after-login.component";
import { AfterLoginRoutes } from "./after-login.routing";
import { RouterModule } from "@angular/router";
import { PartialsModule } from "./partials/partials.module";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { MapModule } from "./component/map/map.module";
import { VillageModule } from "./component/village/village.module";

@NgModule({
  imports: [
    CommonModule,
    PartialsModule,
    WoCommonModule,
    MapModule,
    VillageModule,
    RouterModule.forRoot(AfterLoginRoutes),
  ],
  exports: [AfterLoginComponent],
  declarations: [AfterLoginComponent],
})
export class AfterLoginModule {}
