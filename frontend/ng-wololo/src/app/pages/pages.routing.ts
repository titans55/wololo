import { Routes, RouterModule } from "@angular/router";
import { AfterLoginRoutes } from "./after-login/after-login.routing";
import { AfterLoginComponent } from "./after-login/component/after-login.component";

export const pageRoutes: Routes = [
  {
    path: "game",
    component: AfterLoginComponent,
    children: AfterLoginRoutes,
  },
];

export const PagesRoutes = RouterModule.forChild(pageRoutes);
