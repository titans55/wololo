import { Injectable } from "@angular/core";
import * as gameConfig from "../../../../../../../../../../postgreswololo/wololo/game-config/gameConfig.json";
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
          this.userService.setResourcesOfSelectedVillage(data.newResources);
          this.villageResourcesService.production();
        }
      });
    //   let building_path = $(this).attr('id')
    //   $.ajax({
    //     type: 'POST',
    //     url: '/game/upgrade',
    //     data: {
    //         building_path: building_path,
    //         village_id: villageData.village_id,
    //         firingTime: firingTime,
    //         csrfmiddlewaretoken: csrftoken
    //     },
    //     success:function(data){
    //       if(data['result'] == 'Success'){
    //           console.log(data['newResources'])

    //           if(!building_path.includes('.')){
    //               villageData.buildings[building_path] = data['newBuilding']
    //           }
    //           console.log(data['newResources'])
    //           villageData.buildings.resources = data['newResources']

    //           let targetRow = getTargetBuildingRow(building_path)
    //           targetRow.find(".buildingDetailsSection").html(getProgressBarHtml(building_path))
    //           targetRow.find(".upgradeOrCancelBtn").html(getCnclBtnHtml(building_path))
    //           initProgressBar(building_path)
    //           initCancelButtons()

    //       }else if(data['result'] == 'Fail'){
    //           // alert("Fail")
    //           console.log("WOLOLO")
    //           $('#insufficentResources').modal('show')
    //       }
    //     }
    // })
  }
}
