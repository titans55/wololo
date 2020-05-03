import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { LandingComponent } from "./component/landing.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [LandingComponent],
})
export class LandingModule {}
