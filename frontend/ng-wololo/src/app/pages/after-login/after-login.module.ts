import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AfterLoginComponent } from "./component/after-login.component";
import { AfterLoginRoutes } from "./after-login.routing";
import { RouterModule } from "@angular/router";
import { PartialsModule } from "./partials/partials.module";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { MapModule } from "./component/map/map.module";
import { VillageModule } from "./component/village/village.module";
import { AuthenticatedGlobalService } from "./service/authenticated-global.service";
import { AuthGuard } from "./service/user/guard/auth.guard";

@NgModule({
  imports: [
    CommonModule,
    PartialsModule,
    WoCommonModule,
    MapModule,
    VillageModule,
    RouterModule.forChild(AfterLoginRoutes),
  ],
  exports: [AfterLoginComponent],
  declarations: [AfterLoginComponent],
  providers: [AuthenticatedGlobalService, AuthGuard],
})
export class AfterLoginModule {}
