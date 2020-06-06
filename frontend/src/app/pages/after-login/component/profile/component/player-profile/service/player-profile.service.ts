import { Injectable } from "@angular/core";
import { GlobalService } from "src/app/pages/after-login/service/global.service";
import { PlayerProfileInfoDto } from "../dto/player-profile-info.dto";

@Injectable({
  providedIn: "root",
})
export class PlayerProfileService {
  constructor(private globalService: GlobalService) {}

  getPlayerInfoByUsername(username: string): Promise<PlayerProfileInfoDto> {
    return this.globalService.get("player-profile/" + username);
  }
}
