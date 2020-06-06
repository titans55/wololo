import { Component, OnInit, OnDestroy } from "@angular/core";
import { WoVillageSprite } from "src/app/wo-common/wo-phaser-sprite/wo-phaser-sprite";
import { MapSceneService } from "../../../service/map-scene.service";
import { VillageDetailCardService } from "../service/village-detail-card.service";
import { Subscription } from "rxjs";
import { AfterLoginRoutesEnum } from "src/app/pages/after-login/enum/after-login-routes.enum";

@Component({
  selector: "woo-village-detail-card",
  templateUrl: "./village-detail-card.component.html",
  styleUrls: ["./village-detail-card.component.css"],
})
export class VillageDetailCardComponent implements OnInit, OnDestroy {
  selectedVillage: WoVillageSprite;
  villageSelectedSubscription: Subscription;

  constructor(public villageDetailCardService: VillageDetailCardService) {}

  ngOnInit() {
    this.villageSelectedSubscription = this.villageDetailCardService.villageSelectedSubject.subscribe(
      (selectedVillage: WoVillageSprite) => {
        this.selectedVillage = selectedVillage;
      }
    );
  }

  ngOnDestroy() {
    this.villageSelectedSubscription.unsubscribe();
  }

  get AfterLoginRoutesEnum() {
    return AfterLoginRoutesEnum;
  }
}
