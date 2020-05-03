import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { LandingModule } from "./component/landing/landing.module";
import { RegisterModule } from "./component/register/register.module";
import { BeforeLoginComponent } from "./component/before-login.component";
import { RouterModule } from "@angular/router";
import { BeforeLoginRoutes } from "./before-login.routing";
import { BeforeLoginPartialsModule } from "./before-login-partials/before-login-partials.module";

@NgModule({
  imports: [
    CommonModule,
    WoCommonModule,
    LandingModule,
    RegisterModule,
    BeforeLoginPartialsModule,
    RouterModule.forChild(BeforeLoginRoutes),
  ],
  declarations: [BeforeLoginComponent],
})
export class BeforeLoginModule {}
