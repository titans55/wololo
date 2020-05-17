import { Routes, RouterModule } from "@angular/router";
import { BeforeLoginComponent } from "./component/before-login.component";
import { LandingComponent } from "./component/landing/component/landing.component";
import { RegisterComponent } from "./component/register/component/register.component";

export enum BeforeLoginRoutesEnum {
  LANDING_PAGE = "",
  REGISTER_PAGE = "register",
}

export const BeforeLoginRoutes: Routes = [
  {
    path: "",
    component: BeforeLoginComponent,
    children: [
      {
        path: BeforeLoginRoutesEnum.LANDING_PAGE,
        component: LandingComponent,
      },
      {
        path: BeforeLoginRoutesEnum.REGISTER_PAGE,
        component: RegisterComponent,
      },
    ],
  },
];

export const BeforeLoginRoute = RouterModule.forChild(BeforeLoginRoutes);
