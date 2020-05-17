import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { PagesModule } from "./pages/pages.module";
import { pageRoutes } from "./pages/pages.routing";

const routes: Routes = [
  {
    path: "",
    loadChildren: "./pages/pages.module#PagesModule",
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes), PagesModule],
  exports: [RouterModule],
})
export class AppRoutingModule {}
