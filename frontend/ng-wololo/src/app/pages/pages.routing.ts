import { Routes, RouterModule } from '@angular/router';
import { MapComponent } from './map/component/map.component';

export const pageRoutes: Routes = [
  { 
    path: "map",
    component: MapComponent
  },
];

export const PagesRoutes = RouterModule.forChild(pageRoutes);
