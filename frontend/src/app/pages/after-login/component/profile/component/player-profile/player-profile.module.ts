import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { PlayerProfileComponent } from "./component/player-profile.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { ProfileLayoutModule } from "../../profile-layout/profile-layout.module";
import { RouterModule } from "@angular/router";

@NgModule({
  imports: [CommonModule, RouterModule, ProfileLayoutModule, WoCommonModule],
  declarations: [PlayerProfileComponent],
})
export class PlayerProfileModule {}
