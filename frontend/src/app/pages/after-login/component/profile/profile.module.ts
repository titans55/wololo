import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { PlayerProfileModule } from "./component/player-profile/player-profile.module";
import { VillageProfileModule } from "./component/village-profile/village-profile.module";
import { ProfileLayoutModule } from "./profile-layout/profile-layout.module";

@NgModule({
  imports: [
    CommonModule,
    ProfileLayoutModule,
    PlayerProfileModule,
    VillageProfileModule,
  ],
  declarations: [],
})
export class ProfileModule {}
