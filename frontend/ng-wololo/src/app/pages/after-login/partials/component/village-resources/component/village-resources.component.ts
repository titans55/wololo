import { Component, OnInit } from "@angular/core";
import { VillageResourcesService } from "../service/village-resources.service";

@Component({
  selector: "woo-village-resources",
  templateUrl: "./village-resources.component.html",
  styleUrls: ["./village-resources.component.css"],
})
export class VillageResourcesComponent implements OnInit {
  currentWood: number = 0;
  currentIron: number = 0;
  currentClay: number = 0;

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
  }
}
