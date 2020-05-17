/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { MapVillagesService } from './map-villages.service';

describe('Service: MapVillages', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MapVillagesService]
    });
  });

  it('should ...', inject([MapVillagesService], (service: MapVillagesService) => {
    expect(service).toBeTruthy();
  }));
});
