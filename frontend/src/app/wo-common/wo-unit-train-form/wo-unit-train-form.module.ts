import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { WoUnitTrainFormComponent } from "./component/wo-unit-train-form.component";
import { FormsModule } from "@angular/forms";

@NgModule({
  imports: [CommonModule, FormsModule],
  declarations: [WoUnitTrainFormComponent],
  exports: [WoUnitTrainFormComponent],
})
export class WoUnitTrainFormModule {}
