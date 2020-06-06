import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { VillageProfileComponent } from "./component/village-profile.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { RouterModule } from "@angular/router";
import { ProfileLayoutModule } from "../../profile-layout/profile-layout.module";

@NgModule({
  imports: [CommonModule, RouterModule, ProfileLayoutModule, WoCommonModule],
  declarations: [VillageProfileComponent],
})
export class VillageProfileModule {}
