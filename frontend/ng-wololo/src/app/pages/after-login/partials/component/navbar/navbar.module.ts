import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { NavbarComponent } from "./component/navbar.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { RouterModule } from "@angular/router";
import { VillageResourcesModule } from "../village-resources/village-resources.module";

@NgModule({
  imports: [CommonModule, WoCommonModule, RouterModule],
  exports: [NavbarComponent],
  declarations: [NavbarComponent],
})
export class NavbarModule {}
