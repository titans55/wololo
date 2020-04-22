import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PagesModule } from './pages/pages.module';
import { pageRoutes } from './pages/pages.routing';


const routes: Routes = [
  {
    path: "",
    children: pageRoutes
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes), PagesModule],
  exports: [RouterModule]
})
export class AppRoutingModule { }
