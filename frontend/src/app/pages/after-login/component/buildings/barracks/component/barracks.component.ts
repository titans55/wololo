import { Component, OnInit } from "@angular/core";
import { VillageResourcesService } from "src/app/pages/after-login/partials/component/village-resources/service/village-resources.service";
import { Subscription } from "rxjs";
import { VillageModel } from "../../../village/model/general/village-data.model";
import * as gameConfig from "../../../../../../../../../gameConfig.json";

export type infantryConfigs = typeof gameConfig.units.infantry;

@Component({
  selector: "wo-barracks",
  templateUrl: "./barracks.component.html",
  styleUrls: ["./barracks.component.css"],
})
export class BarracksComponent implements OnInit {
  readonly infantryConfigs: infantryConfigs = gameConfig.units.infantry;
  public villagesOfPlayer: Array<VillageModel>;
  private villagesOfPlayerSubscription: Subscription;

  constructor(private villageResourcesService: VillageResourcesService) {}

  ngOnInit() {
    console.log(this.infantryConfigs);
    this.villagesOfPlayerSubscription = this.villageResourcesService.villagesOfPlayerSubject.subscribe(
      (villages) => {
        this.villagesOfPlayer = villages;
        console.log(this.villagesOfPlayer);
      }
    );
  }

  get selectedVillage(): VillageModel {
    if (this.villagesOfPlayer) {
      return this.villagesOfPlayer.find((village) => village.selected);
    } else {
      return null;
    }
  }
}
