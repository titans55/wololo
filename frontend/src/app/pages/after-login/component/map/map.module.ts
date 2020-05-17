import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { MapComponent } from "./component/map.component";
import { MapSceneService } from "./service/map-scene.service";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { VillageDetailCardModule } from "./component/village-detail-card/village-detail-card.module";

@NgModule({
  imports: [CommonModule, WoCommonModule, VillageDetailCardModule],
  declarations: [MapComponent],
  providers: [],
})
export class MapModule {}
