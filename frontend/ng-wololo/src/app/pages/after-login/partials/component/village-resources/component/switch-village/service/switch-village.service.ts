import { Injectable } from "@angular/core";
import { VillageResourcesService } from "../../../service/village-resources.service";

@Injectable({
  providedIn: "root",
})
export class SwitchVillageService {
  constructor(private villageResourcesService: VillageResourcesService) {}

  async switchVillageButton(villageIndex: number): Promise<void> {
    await this.villageResourcesService.initPlayer(villageIndex);
  }
}
