import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { VillageComponent } from "./component/village.component";
import { VillageService } from "./service/village.service";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { RouterModule } from "@angular/router";

@NgModule({
  imports: [CommonModule, WoCommonModule, RouterModule],
  declarations: [VillageComponent],
  providers: [VillageService],
})
export class VillageModule {}
