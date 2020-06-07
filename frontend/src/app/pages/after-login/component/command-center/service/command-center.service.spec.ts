/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { CommandCenterService } from './command-center.service';

describe('Service: CommandCenter', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CommandCenterService]
    });
  });

  it('should ...', inject([CommandCenterService], (service: CommandCenterService) => {
    expect(service).toBeTruthy();
  }));
});
