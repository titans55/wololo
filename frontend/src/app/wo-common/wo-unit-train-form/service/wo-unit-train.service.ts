import { Injectable } from "@angular/core";
import { GlobalService } from "../../../pages/after-login/service/global.service";
import { UnitTrainFormModel } from "../model/unit-train-form.model";
import { VillageUnitType } from "../type/unit-types.type";
import { UnitTrainResponseDto } from "./dto/unit-train-response-dto";
import { UserService } from "src/app/pages/after-login/service/user/user.service";
import { VillageResourcesService } from "src/app/pages/after-login/partials/component/village-resources/service/village-resources.service";

@Injectable()
export class WoUnitTrainService {
  constructor(
    private globalService: GlobalService,
    private userService: UserService,
    private villageResourcesService: VillageResourcesService
  ) {}

  train(
    url: string,
    unitTrainForm: UnitTrainFormModel<VillageUnitType>
  ): Promise<any> {
    return this.globalService
      .post(url, unitTrainForm)
      .then((unitTrainResponseDto: UnitTrainResponseDto) => {
        if (unitTrainResponseDto.result == "Success") {
          console.log(unitTrainResponseDto);
          this.userService.setTroopsOfVillageById(
            unitTrainForm.villageId,
            unitTrainResponseDto.newTroops
          );
          this.userService.setBuildingOfSelectedVIllage(
            "resources",
            unitTrainResponseDto.newResources
          );
          this.villageResourcesService.production();
        } else {
          console.error(
            "validation not passed during training unit on serverside"
          );
        }
      });
  }
}
