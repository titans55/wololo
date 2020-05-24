import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BarracksComponent } from "./component/barracks.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [BarracksComponent],
})
export class BarracksModule {}
