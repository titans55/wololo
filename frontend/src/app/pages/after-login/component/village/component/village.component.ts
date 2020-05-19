import { Component, OnInit } from "@angular/core";
import { VillageService } from "../service/village.service";
import { VillageResourcesService } from "../../../partials/component/village-resources/service/village-resources.service";
import {
  VillageModel,
  BuildingsConfigs,
  Resources,
} from "../model/general/village-data.model";
import {
  ResourcesBuildings,
  SelectedVillageBuildings,
  BaseBuilding,
  Upgrading,
  ResourceBuildingDetails,
} from "../model/general/village.dto";
import { Subscription } from "rxjs";

@Component({
  selector: "woo-village",
  templateUrl: "./village.component.html",
  styleUrls: ["./village.component.css"],
})
export class VillageComponent implements OnInit {
  public villagesOfPlayer: Array<VillageModel>;
  private villagesOfPlayerSubscription: Subscription;

  constructor(
    private service: VillageService,
    private villageResourcesService: VillageResourcesService
  ) {}

  ngOnInit() {
    this.villagesOfPlayerSubscription = this.villageResourcesService.villagesOfPlayerSubject.subscribe(
      (villages) => {
        this.villagesOfPlayer = villages;
        console.log(this.villagesOfPlayer);
      }
    );
  }

  ngOnDestroy() {
    // unsubscribe to ensure no memory leaks
    this.villagesOfPlayerSubscription.unsubscribe();
  }

  getBuildingNeededResources(
    buildingNames: keyof SelectedVillageBuildings,
    resourceBuildingName?: keyof ResourcesBuildings
  ): Resources<number> {
    return this.service.getBuildingNeededResources(
      this.selectedVillage,
      buildingNames,
      resourceBuildingName
    );
  }

  getBuildingUpgradeTime(
    buildingNames: keyof SelectedVillageBuildings,
    resourceBuildingName?: keyof ResourcesBuildings
  ): string {
    return this.service.getBuildingUpgradeTime(
      this.selectedVillage,
      buildingNames,
      resourceBuildingName
    );
  }

  get upgradeTime(): string {
    return "";
  }

  get selectedVillage(): VillageModel {
    if (this.villagesOfPlayer) {
      return this.villagesOfPlayer.find((village) => village.selected);
    } else {
      return null;
    }
  }
  onUpgrade(buildingPath: string) {
    this.service.upgradeBuilding(buildingPath);
  }
}
