import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BeforeLoginFooterComponent } from "./component/before-login-footer/before-login-footer.component";
import { BeforeLoginNavbarComponent } from "./component/before-login-navbar/before-login-navbar.component";

@NgModule({
  imports: [CommonModule],
  declarations: [BeforeLoginFooterComponent, BeforeLoginNavbarComponent],
  exports: [BeforeLoginFooterComponent, BeforeLoginNavbarComponent],
})
export class BeforeLoginPartialsModule {}
