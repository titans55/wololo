import { Injectable } from "@angular/core";
import * as gameConfig from "../../../../../../../../gameConfig.json";
import { GlobalService } from "../../../service/global.service";
import {
  BuildingsConfigs,
  Resources,
  VillageModel,
} from "../model/general/village-data.model";
import {
  SelectedVillageBuildings,
  ResourcesBuildings,
} from "../model/general/village.dto";
import { calculateHumanizedTimeFromMinutes } from "../../../../../utils/date-util/date-util";
import { UserService } from "../../../service/user/user.service";
import { SelectedVillageModel } from "../../../service/user/model/selected-village.model";
import { VillageResourcesService } from "../../../partials/component/village-resources/service/village-resources.service";

@Injectable({
  providedIn: "root",
})
export class VillageService {
  public buildingsConfigs: BuildingsConfigs = gameConfig.buildings;

  constructor(
    private globalService: GlobalService,
    private userService: UserService,
    private villageResourcesService: VillageResourcesService
  ) {}

  getBuildingNeededResources(
    selectedVillage: VillageModel,
    buildingNames: keyof SelectedVillageBuildings,
    resourceBuildingName?: keyof ResourcesBuildings
  ): Resources<number> {
    let neededResources: Resources<number>;
    if (buildingNames == "resources") {
      neededResources = this.buildingsConfigs.resources[resourceBuildingName]
        .upgradingCosts[
        selectedVillage.buildings.resources[resourceBuildingName].level + 1
      ];
    } else {
      neededResources = this.buildingsConfigs[buildingNames].upgradingCosts[
        selectedVillage.buildings[buildingNames].level + 1
      ];
    }
    if (neededResources == null) {
      throw "Needed resources can't be null";
    }
    return neededResources;
  }

  getBuildingUpgradeTime(
    selectedVillage: VillageModel,
    buildingNames: keyof SelectedVillageBuildings,
    resourceBuildingName?: keyof ResourcesBuildings
  ): string {
    let upgradingMinutes: number;
    let upgradingTimeLabel: string;
    if (buildingNames == "resources") {
      upgradingMinutes = this.buildingsConfigs.resources[resourceBuildingName]
        .upgradeTime[
        selectedVillage.buildings.resources[resourceBuildingName].level + 1
      ];
    } else {
      upgradingMinutes = this.buildingsConfigs[buildingNames].upgradeTime[
        selectedVillage.buildings[buildingNames].level + 1
      ];
    }
    if (upgradingMinutes == null) {
      throw "Upgrading time can't be null";
    }
    upgradingTimeLabel = calculateHumanizedTimeFromMinutes(upgradingMinutes);
    return upgradingTimeLabel;
  }

  upgradeBuilding(buildingPath: string): void {
    console.log(buildingPath);
    let selectedVillageInfo: SelectedVillageModel = this.userService.getSelectedVillageInfo();
    this.globalService
      .post("upgrade-building/" + selectedVillageInfo.villageIndex, {
        villageId: selectedVillageInfo.villageId,
        buildingPath: buildingPath,
      })
      .then((data: any) => {
        //TODO write model here
        if (data.result == "Success") {
          if(!buildingPath.includes(".")){
            this.userService.setBuildingOfSelectedVIllage(<keyof SelectedVillageBuildings>buildingPath, data.newBuilding)
          }
          this.userService.setBuildingOfSelectedVIllage("resources", data.newResources)
          this.villageResourcesService.production();
        }
      });
  }
}
