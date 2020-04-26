import { Component, OnInit } from "@angular/core";
import { SwitchVillageService } from "../service/switch-village.service";
import { VillageResourcesService } from "../../../service/village-resources.service";
import { VillageModel } from "src/app/pages/after-login/component/village/model/village-data.model";

@Component({
  selector: "woo-switch-village",
  templateUrl: "./switch-village.component.html",
  styleUrls: ["./switch-village.component.css"],
})
export class SwitchVillageComponent implements OnInit {
  public villagesOfPlayer: Array<VillageModel>;

  constructor(
    public service: SwitchVillageService,
    private villageResourcesService: VillageResourcesService
  ) {}

  ngOnInit() {
    this.villageResourcesService.villagesOfPlayerSubject.subscribe(
      (villages) => {
        this.villagesOfPlayer = villages;
        this.setSelectedVillageName();
      }
    );
  }

  villageSelectClick(villageIndex: number) {
    this.service.switchVillageButton(villageIndex).then(() => {
      console.log(this.villagesOfPlayer);
      this.setSelectedVillageName();
    });
  }

  selectedVillageName: string;
  private setSelectedVillageName() {
    this.selectedVillageName = this.villagesOfPlayer.find((village) => {
      return village.selected;
    }).villageName;
  }
}
