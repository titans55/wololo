/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { SwitchVillageService } from './switch-village.service';

describe('Service: SwitchVillage', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SwitchVillageService]
    });
  });

  it('should ...', inject([SwitchVillageService], (service: SwitchVillageService) => {
    expect(service).toBeTruthy();
  }));
});
