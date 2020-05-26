import { Component, OnInit, OnDestroy } from "@angular/core";
import { SwitchVillageService } from "../service/switch-village.service";
import { VillageResourcesService } from "../../../service/village-resources.service";
import { VillageModel } from "src/app/pages/after-login/component/village/model/general/village-data.model";
import { Subscription } from "rxjs";

@Component({
  selector: "woo-switch-village",
  templateUrl: "./switch-village.component.html",
  styleUrls: ["./switch-village.component.css"],
})
export class SwitchVillageComponent implements OnInit, OnDestroy {
  public villagesOfPlayer: Array<VillageModel>;
  private subscription: Subscription;

  constructor(
    public service: SwitchVillageService,
    private villageResourcesService: VillageResourcesService
  ) {}

  ngOnInit() {
    this.subscription = this.villageResourcesService.villagesOfPlayerSubject.subscribe(
      (villages) => {
        this.villagesOfPlayer = villages;
        this.setSelectedVillageName();
      }
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  villageSelectClick(villageIndex: number) {
    this.service.switchVillageButton(villageIndex).then(() => {
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
