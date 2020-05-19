import { Component, OnInit } from "@angular/core";
import { VillageResourcesService } from "../service/village-resources.service";
import {
  VillageResourceDetailModel,
  PopulationModel,
} from "src/app/pages/after-login/component/village/model/general/village-data.model";
import { Subject, Subscription } from "rxjs";

@Component({
  selector: "woo-village-resources",
  templateUrl: "./village-resources.component.html",
  styleUrls: ["./village-resources.component.css"],
})
export class VillageResourcesComponent implements OnInit {
  subscriptions: Subscription = new Subscription();
  currentWood: VillageResourceDetailModel;
  currentIron: VillageResourceDetailModel;
  currentClay: VillageResourceDetailModel;
  storageCapacity: number;
  populationInfo: PopulationModel;

  constructor(public villageResourcesService: VillageResourcesService) {}

  ngOnInit() {
    this.subscriptions.add(
      this.villageResourcesService.wood.currentSummary.subscribe(
        (currentWood) => {
          this.currentWood = currentWood;
        }
      )
    );
    this.subscriptions.add(
      this.villageResourcesService.iron.currentSummary.subscribe(
        (currentIron) => {
          this.currentIron = currentIron;
        }
      )
    );
    this.subscriptions.add(
      this.villageResourcesService.clay.currentSummary.subscribe(
        (currentClay) => {
          this.currentClay = currentClay;
        }
      )
    );
    this.subscriptions.add(
      this.villageResourcesService.storageSubject.subscribe(
        (storageCapacity) => {
          this.storageCapacity = storageCapacity;
        }
      )
    );
    this.subscriptions.add(
      this.villageResourcesService.populationSubject.subscribe(
        (populationInfo) => {
          this.populationInfo = populationInfo;
        }
      )
    );
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }
}
