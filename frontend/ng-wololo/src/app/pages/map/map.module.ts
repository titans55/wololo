import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MapComponent } from './component/map.component';
import { MapSceneService } from './service/map-scene.service';
import { WoCommonModule } from 'src/app/wo-common/wo-common.module';

@NgModule({
  imports: [
    CommonModule,
    WoCommonModule
  ],
  declarations: [MapComponent],
  providers: [MapSceneService]
})
export class MapModule { }
