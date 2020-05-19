import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { PhaserModule } from "phaser-component-library";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { HumanizeCamelCasePipe } from "./pipe/humanize-camel-case.pipe";
import { WoProgressBarModule } from "./wo-progress-bar/wo-progress-bar.module";

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    PhaserModule,
    NgbModule,
    WoProgressBarModule,
  ],
  exports: [
    FormsModule,
    PhaserModule,
    NgbModule,
    HumanizeCamelCasePipe,
    WoProgressBarModule,
  ],
  declarations: [HumanizeCamelCasePipe],
})
export class WoCommonModule {}
