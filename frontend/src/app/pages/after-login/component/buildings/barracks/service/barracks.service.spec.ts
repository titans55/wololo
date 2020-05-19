/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { BarracksService } from './barracks.service';

describe('Service: Barracks', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BarracksService]
    });
  });

  it('should ...', inject([BarracksService], (service: BarracksService) => {
    expect(service).toBeTruthy();
  }));
});
