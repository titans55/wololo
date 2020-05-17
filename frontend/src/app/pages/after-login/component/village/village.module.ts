import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { VillageComponent } from "./component/village.component";
import { VillageService } from "./service/village.service";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [VillageComponent],
  providers: [VillageService],
})
export class VillageModule {}
