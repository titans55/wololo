import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { VillageResourcesComponent } from "./component/village-resources.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { SwitchVillageModule } from "./component/switch-village/switch-village.module";

@NgModule({
  imports: [CommonModule, WoCommonModule, SwitchVillageModule],
  declarations: [VillageResourcesComponent],
  exports: [VillageResourcesComponent],
})
export class VillageResourcesModule {}
