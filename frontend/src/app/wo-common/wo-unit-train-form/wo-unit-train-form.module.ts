import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { WoUnitTrainFormComponent } from "./component/wo-unit-train-form.component";
import { FormsModule } from "@angular/forms";
import { WoUnitTrainService } from "./service/wo-unit-train.service";

@NgModule({
  imports: [CommonModule, FormsModule],
  declarations: [WoUnitTrainFormComponent],
  exports: [WoUnitTrainFormComponent],
  providers: [WoUnitTrainService],
})
export class WoUnitTrainFormModule {}
