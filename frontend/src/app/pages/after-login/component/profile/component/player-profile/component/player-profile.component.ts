import { Component, OnInit } from "@angular/core";
import { PlayerProfileService } from "../service/player-profile.service";
import { PlayerProfileInfoDto } from "../dto/player-profile-info.dto";
import { ActivatedRoute } from "@angular/router";
import { PlayerProfileRoutesEnum } from "../enum/player-profile-routes.enum";
import { AfterLoginRoutes } from "src/app/pages/after-login/after-login.routing";
import { AfterLoginRoutesEnum } from "src/app/pages/after-login/enum/after-login-routes.enum";

@Component({
  selector: "wo-player-profile",
  templateUrl: "./player-profile.component.html",
  styleUrls: ["./player-profile.component.css"],
})
export class PlayerProfileComponent implements OnInit {
  usernameFromUrlParam: string;
  playerProfileInfo: PlayerProfileInfoDto;
  constructor(
    private route: ActivatedRoute,
    private service: PlayerProfileService
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(async (params) => {
      try {
        this.usernameFromUrlParam = params.get(
          PlayerProfileRoutesEnum.USERNAME_URL_PARAM
        );
        this.service
          .getPlayerInfoByUsername(this.usernameFromUrlParam)
          .then((playerProfileInfo) => {
            this.playerProfileInfo = playerProfileInfo;
          });
      } catch {
        this.usernameFromUrlParam = undefined;
      }
    });
  }

  get AfterLoginRoutesEnum() {
    return AfterLoginRoutesEnum;
  }
}
