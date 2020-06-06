import { Injectable } from "@angular/core";
import { GlobalService } from "src/app/pages/after-login/service/global.service";
import { VillageProfileInfoDto } from "../dto/village-profile-info.dto";

@Injectable({
  providedIn: "root",
})
export class VillageProfileService {
  constructor(private globalService: GlobalService) {}

  getVillageProfileById(villageId: number): Promise<VillageProfileInfoDto> {
    return this.globalService.get("village-profile/" + villageId);
  }
}
