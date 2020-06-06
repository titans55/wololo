import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { VillageProfileComponent } from "./component/village-profile.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [VillageProfileComponent],
})
export class VillageProfileModule {}
