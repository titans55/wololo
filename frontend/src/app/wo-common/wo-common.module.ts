import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { PhaserModule } from "phaser-component-library";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { HumanizeCamelCasePipe } from "./pipe/humanize-camel-case.pipe";

@NgModule({
  imports: [CommonModule, FormsModule, PhaserModule, NgbModule],
  exports: [FormsModule, PhaserModule, NgbModule, HumanizeCamelCasePipe],
  declarations: [HumanizeCamelCasePipe],
})
export class WoCommonModule {}
