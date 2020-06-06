import { Injectable } from "@angular/core";
import { GlobalService } from "src/app/pages/after-login/service/global.service";
import { PlayerProfileDto } from "../dto/player-profile-info.dto";

@Injectable({
  providedIn: "root",
})
export class PlayerProfileService {
  constructor(private globalService: GlobalService) {}

  getPlayerProfileByUsername(username: string): Promise<PlayerProfileDto> {
    return this.globalService.get("player-profile/" + username);
  }
}
