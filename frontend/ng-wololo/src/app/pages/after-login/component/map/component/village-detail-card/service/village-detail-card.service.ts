import { Injectable } from "@angular/core";
import { WoVillageSprite } from "src/app/wo-common/wo-phaser-sprite/wo-phaser-sprite";
import { Subject, Observable } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class VillageDetailCardService {
  villageSelectedSubject: Subject<WoVillageSprite>;

  constructor() {
    this.villageSelectedSubject = new Subject();
  }

  villageSelected(woVillageSprite: WoVillageSprite) {
    this.villageSelectedSubject.next(woVillageSprite);
  }
}
