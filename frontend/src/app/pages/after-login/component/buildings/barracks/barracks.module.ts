import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BarracksComponent } from "./component/barracks.component";
import { BarracksService } from "./service/barracks.service";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [BarracksComponent],
  providers: [BarracksService],
})
export class BarracksModule {}
