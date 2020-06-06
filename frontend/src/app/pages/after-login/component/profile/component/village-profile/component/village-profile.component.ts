import { Component, OnInit } from "@angular/core";
import { VillageProfileService } from "../service/village-profile.service";
import { ActivatedRoute } from "@angular/router";
import { VillageProfileRoutesEnum } from "../enum/village-profile-routes.enum";
import { VillageProfileInfoDto } from "../dto/village-profile-info.dto";
import { AfterLoginRoutesEnum } from "src/app/pages/after-login/enum/after-login-routes.enum";

@Component({
  selector: "wo-village-profile",
  templateUrl: "./village-profile.component.html",
  styleUrls: ["./village-profile.component.css"],
})
export class VillageProfileComponent implements OnInit {
  villageIdFromUrlParam: number;
  villageProfileInfo: VillageProfileInfoDto;

  constructor(
    private route: ActivatedRoute,
    private service: VillageProfileService
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(async (params) => {
      try {
        this.villageIdFromUrlParam = parseInt(
          params.get(VillageProfileRoutesEnum.VILLAGE_ID_URL_PARAM)
        );
        this.service
          .getVillageProfileById(this.villageIdFromUrlParam)
          .then((villageProfileInfo) => {
            this.villageProfileInfo = villageProfileInfo;
            console.log(this.villageProfileInfo);
          });
      } catch {
        this.villageIdFromUrlParam = undefined;
        this.villageProfileInfo = undefined;
      }
    });
  }

  get AfterLoginRoutesEnum() {
    return AfterLoginRoutesEnum;
  }
}
