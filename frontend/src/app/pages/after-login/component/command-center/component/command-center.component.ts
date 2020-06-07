import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { CommandCenterService } from "../service/command-center.service";
import { VillageProfileRoutesEnum } from "../../profile/component/village-profile/enum/village-profile-routes.enum";

@Component({
  selector: "wo-command-center",
  templateUrl: "./command-center.component.html",
  styleUrls: ["./command-center.component.css"],
})
export class CommandCenterComponent implements OnInit {
  villageIdFromUrlParam: number;

  constructor(
    private route: ActivatedRoute,
    private service: CommandCenterService
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(async (params) => {
      try {
        this.villageIdFromUrlParam = parseInt(
          params.get(VillageProfileRoutesEnum.VILLAGE_ID_URL_PARAM)
        );
        // this.service
        //   .getVillageProfileById(this.villageIdFromUrlParam)
        //   .then((villageProfileInfo) => {
        //     this.villageProfileInfo = villageProfileInfo;
        //     console.log(this.villageProfileInfo);
        //   });
      } catch {
        this.villageIdFromUrlParam = undefined;
        // this.villageProfileInfo = undefined;
      }
    });
  }
}
