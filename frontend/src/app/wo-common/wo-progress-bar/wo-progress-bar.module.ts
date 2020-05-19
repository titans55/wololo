import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { WoProgressBarComponent } from "./component/wo-progress-bar.component";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";

@NgModule({
  imports: [CommonModule, NgbModule],
  declarations: [WoProgressBarComponent],
  exports: [WoProgressBarComponent],
})
export class WoProgressBarModule {}
