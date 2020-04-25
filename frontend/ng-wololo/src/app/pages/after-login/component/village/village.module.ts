import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { VillageComponent } from "./component/village.component";
import { VillageService } from "./service/village.service";

@NgModule({
  imports: [CommonModule],
  declarations: [VillageComponent],
  providers: [VillageService],
})
export class VillageModule {}
