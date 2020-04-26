import { Component, OnInit } from "@angular/core";
import { VillageResourcesService } from "../service/village-resources.service";
import {
  VillageResourceDetailModel,
  PopulationModel,
} from "src/app/pages/after-login/component/village/model/village-data.model";
import { Subject } from "rxjs";

@Component({
  selector: "woo-village-resources",
  templateUrl: "./village-resources.component.html",
  styleUrls: ["./village-resources.component.css"],
})
export class VillageResourcesComponent implements OnInit {
  currentWood: VillageResourceDetailModel;
  currentIron: VillageResourceDetailModel;
  currentClay: VillageResourceDetailModel;
  storageCapacity: number;
  populationInfo: PopulationModel;

  constructor(public villageResourcesService: VillageResourcesService) {}

  ngOnInit() {
    this.villageResourcesService.wood.currentSummary.subscribe(
      (currentWood) => {
        this.currentWood = currentWood;
      }
    );
    this.villageResourcesService.iron.currentSummary.subscribe(
      (currentIron) => {
        this.currentIron = currentIron;
      }
    );
    this.villageResourcesService.clay.currentSummary.subscribe(
      (currentClay) => {
        this.currentClay = currentClay;
      }
    );
    this.villageResourcesService.storageSubject.subscribe((storageCapacity) => {
      this.storageCapacity = storageCapacity;
    });
    this.villageResourcesService.populationSubject.subscribe(
      (populationInfo) => {
        this.populationInfo = populationInfo;
      }
    );
  }
}
