/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { MapSceneService } from './map-scene.service';

describe('Service: MapScene', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MapSceneService]
    });
  });

  it('should ...', inject([MapSceneService], (service: MapSceneService) => {
    expect(service).toBeTruthy();
  }));
});
