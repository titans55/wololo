import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { AfterLoginModule } from "./after-login/after-login.module";
import { BeforeLoginModule } from "./before-login/before-login.module";
import { RouterModule } from "@angular/router";
import { pageRoutes } from "./pages.routing";

@NgModule({
  imports: [
    CommonModule,
    BeforeLoginModule,
    AfterLoginModule,
    RouterModule.forChild(pageRoutes),
  ],
  declarations: [],
})
export class PagesModule {}
