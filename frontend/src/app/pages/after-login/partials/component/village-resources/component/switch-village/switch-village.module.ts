import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { SwitchVillageComponent } from "./component/switch-village.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [SwitchVillageComponent],
  exports: [SwitchVillageComponent],
})
export class SwitchVillageModule {}
