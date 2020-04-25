import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { VillageResourcesComponent } from "./component/village-resources.component";

@NgModule({
  imports: [CommonModule],
  declarations: [VillageResourcesComponent],
  exports: [VillageResourcesComponent],
})
export class VillageResourcesModule {}
