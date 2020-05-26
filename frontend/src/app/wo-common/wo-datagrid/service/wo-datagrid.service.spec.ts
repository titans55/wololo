/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { WoDatagridService } from './wo-datagrid.service';

describe('Service: WoDatagrid', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WoDatagridService]
    });
  });

  it('should ...', inject([WoDatagridService], (service: WoDatagridService) => {
    expect(service).toBeTruthy();
  }));
});
