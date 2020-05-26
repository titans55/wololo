import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AfterLoginComponent } from "./component/after-login.component";
import { AfterLoginRoutes } from "./after-login.routing";
import { RouterModule } from "@angular/router";
import { PartialsModule } from "./partials/partials.module";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { MapModule } from "./component/map/map.module";
import { VillageModule } from "./component/village/village.module";
import { GlobalService } from "./service/global.service";
import { AuthGuard } from "./service/user/guard/auth.guard";
import { UserService } from "./service/user/user.service";
import { HTTP_INTERCEPTORS } from "@angular/common/http";
import { DateConverterInterceptor } from "./service/date-converter-http-interceptor/date-converter-http-interceptor";
import { BuildingsModule } from "./component/buildings/buildings.module";
import { RankingModule } from "./component/ranking/ranking.module";
import { ReportsModule } from "./component/reports/reports.module";

@NgModule({
  imports: [
    CommonModule,
    PartialsModule,
    WoCommonModule,
    MapModule,
    VillageModule,
    BuildingsModule,
    RankingModule,
    ReportsModule,
    RouterModule.forChild(AfterLoginRoutes),
  ],
  exports: [AfterLoginComponent],
  declarations: [AfterLoginComponent],
  providers: [
    AuthGuard,
    UserService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: DateConverterInterceptor,
      multi: true,
    },
  ],
})
export class AfterLoginModule {}
