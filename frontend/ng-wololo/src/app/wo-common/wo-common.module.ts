import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { PhaserModule } from "phaser-component-library";

@NgModule({
  imports: [CommonModule, FormsModule, PhaserModule],
  exports: [FormsModule, PhaserModule],
  declarations: [],
})
export class WoCommonModule {}
