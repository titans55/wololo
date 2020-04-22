import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MapComponent } from './component/map.component';
import { MapSceneService } from './service/map-scene.service';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [MapComponent],
  providers: [MapSceneService]
})
export class MapModule { }
