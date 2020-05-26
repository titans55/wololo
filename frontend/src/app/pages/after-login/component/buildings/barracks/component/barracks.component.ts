import { Component, OnInit, OnDestroy } from "@angular/core";
import { VillageResourcesService } from "src/app/pages/after-login/partials/component/village-resources/service/village-resources.service";
import { Subscription } from "rxjs";
import { VillageModel } from "../../../village/model/general/village-data.model";
import * as gameConfig from "../../../../../../../../../gameConfig.json";
import { UnitTrainFormModel } from "src/app/wo-common/wo-unit-train-form/model/unit-train-form.model";
import { InVillageInfantry } from "../../../village/model/general/village.dto";
import { BarracksConfigsEnum } from "../enum/barracks-configs.enum";

export type infantryConfigs = typeof gameConfig.units.infantry;

@Component({
  selector: "wo-barracks",
  templateUrl: "./barracks.component.html",
  styleUrls: ["./barracks.component.css"],
})
export class BarracksComponent implements OnInit, OnDestroy {
  readonly infantryConfigs: infantryConfigs = gameConfig.units.infantry;
  public selectedVillage: VillageModel;
  private villagesOfPlayerSubscription: Subscription;

  constructor(private villageResourcesService: VillageResourcesService) {}

  ngOnInit() {
    console.log(this.infantryConfigs);
    this.villagesOfPlayerSubscription = this.villageResourcesService.villagesOfPlayerSubject.subscribe(
      (villages) => {
        this.selectedVillage = villages.find((village) => village.selected);
        console.log("changed village");
      }
    );
  }

  ngOnDestroy() {
    this.villagesOfPlayerSubscription.unsubscribe();
  }

  get BarracksConfigsEnum() {
    return BarracksConfigsEnum;
  }
}
