import { Routes, RouterModule } from "@angular/router";
import { AfterLoginRoutes } from "./after-login/after-login.routing";
import { AfterLoginComponent } from "./after-login/component/after-login.component";
import { BeforeLoginComponent } from "./before-login/component/before-login.component";
import {
  BeforeLoginRoutes,
  BeforeLoginRoutesEnum,
} from "./before-login/before-login.routing";
import { LandingComponent } from "./before-login/component/landing/component/landing.component";

export const pageRoutes: Routes = [
  {
    path: "",
    children: BeforeLoginRoutes,
  },
  {
    path: "game",
    children: AfterLoginRoutes,
  },
];

export const PagesRoutes = RouterModule.forChild(pageRoutes);
