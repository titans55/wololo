/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { VillageDetailCardService } from './village-detail-card.service';

describe('Service: VillageDetailCard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [VillageDetailCardService]
    });
  });

  it('should ...', inject([VillageDetailCardService], (service: VillageDetailCardService) => {
    expect(service).toBeTruthy();
  }));
});
