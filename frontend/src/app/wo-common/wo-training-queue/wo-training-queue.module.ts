import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { WoTrainingQueueComponent } from "./component/wo-training-queue.component";
import { WoCountdownComponent } from "../wo-countdown/wo-countdown.component";

@NgModule({
  imports: [CommonModule],
  declarations: [WoTrainingQueueComponent, WoCountdownComponent],
  exports: [WoTrainingQueueComponent, WoCountdownComponent],
})
export class WoTrainingQueueModule {}
