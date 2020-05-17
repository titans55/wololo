/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { VillageResourcesService } from './village-resources.service';

describe('Service: VillageResources', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [VillageResourcesService]
    });
  });

  it('should ...', inject([VillageResourcesService], (service: VillageResourcesService) => {
    expect(service).toBeTruthy();
  }));
});
