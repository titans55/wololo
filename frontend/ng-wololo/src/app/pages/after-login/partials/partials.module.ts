import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { NavbarModule } from "./component/navbar/navbar.module";
import { FooterModule } from "./component/footer/footer.module";
import { VillageResourcesModule } from "./component/village-resources/village-resources.module";

@NgModule({
  imports: [CommonModule, NavbarModule, FooterModule, VillageResourcesModule],
  exports: [NavbarModule, FooterModule, VillageResourcesModule],
  declarations: [],
})
export class PartialsModule {}
