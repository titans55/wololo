import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { VillageDetailCardComponent } from "./component/village-detail-card.component";
import { VillageDetailCardService } from "./service/village-detail-card.service";
@NgModule({
  imports: [CommonModule],
  declarations: [VillageDetailCardComponent],
  exports: [VillageDetailCardComponent],
  providers: [VillageDetailCardService],
})
export class VillageDetailCardModule {}
