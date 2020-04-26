import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { PhaserModule } from "phaser-component-library";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";

@NgModule({
  imports: [CommonModule, FormsModule, PhaserModule, NgbModule],
  exports: [FormsModule, PhaserModule, NgbModule],
  declarations: [],
})
export class WoCommonModule {}
