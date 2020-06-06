/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { VillageProfileService } from './village-profile.service';

describe('Service: VillageProfile', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [VillageProfileService]
    });
  });

  it('should ...', inject([VillageProfileService], (service: VillageProfileService) => {
    expect(service).toBeTruthy();
  }));
});
