import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BarracksModule } from "./barracks/barracks.module";

@NgModule({
  imports: [CommonModule, BarracksModule],
  declarations: [],
  exports: [BarracksModule],
})
export class BuildingsModule {}
