/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from "@angular/core/testing";
import { WoUnitTrainService } from "./wo-unit-train.service";

describe("Service: WoUnitTrainService", () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WoUnitTrainService],
    });
  });

  it("should ...", inject(
    [WoUnitTrainService],
    (service: WoUnitTrainService) => {
      expect(service).toBeTruthy();
    }
  ));
});
