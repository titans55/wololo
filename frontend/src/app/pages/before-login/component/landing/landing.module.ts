import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { LandingComponent } from "./component/landing.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { LoginFormComponent } from "./component/login-form/login-form.component";
import { ReactiveFormsModule } from "@angular/forms";

@NgModule({
  imports: [CommonModule, WoCommonModule, ReactiveFormsModule],
  declarations: [LandingComponent, LoginFormComponent],
})
export class LandingModule {}
