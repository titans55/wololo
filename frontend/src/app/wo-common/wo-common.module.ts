import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { PhaserModule } from "phaser-component-library";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { WoProgressBarModule } from "./wo-progress-bar/wo-progress-bar.module";
import { WoUnitTrainFormModule } from "./wo-unit-train-form/wo-unit-train-form.module";
import { WoTrainingQueueModule } from "./wo-training-queue/wo-training-queue.module";
import { WoDatagridModule } from "./wo-datagrid/wo-datagrid.module";
import { WoPipesModule } from "./pipe/wo-pipes.module";

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    PhaserModule,
    NgbModule,
    WoProgressBarModule,
    WoUnitTrainFormModule,
    WoTrainingQueueModule,
    WoDatagridModule,
    WoPipesModule,
  ],
  exports: [
    FormsModule,
    PhaserModule,
    NgbModule,
    WoProgressBarModule,
    WoUnitTrainFormModule,
    WoTrainingQueueModule,
    WoDatagridModule,
    WoPipesModule,
  ],
})
export class WoCommonModule {}
