import { Component } from "@angular/core";
import { DataSourceConfigs } from "src/app/wo-common/wo-datagrid/service/wo-datagrid.service";
import { RankingConfigsEnum } from "../enum/ranking-configs.enum";
import { GlobalService } from "../../../service/global.service";
import { AfterLoginRoutesEnum } from "../../../enum/after-login-routes.enum";

@Component({
  selector: "wo-ranking",
  templateUrl: "./ranking.component.html",
  styleUrls: ["./ranking.component.css"],
})
export class RankingComponent {
  readonly dataSourceConfigs: DataSourceConfigs = {
    endpoint: this.globalService.getEndpointUrl(
      RankingConfigsEnum.PLAYER_RANKING_ENDPOINT
    ),
    httpOptions: this.globalService.httpOptions,
    columns: [
      {
        dataKey: "ranking",
      },
      {
        dataKey: "username",
        includeHrefConfigs: {
          enabled: true,
          redirectionUrl: "game/" + AfterLoginRoutesEnum.PLAYER_PROFILE,
          parameterColumn: "username",
        },
      },
      {
        dataKey: "numberOfVillages",
      },
      {
        dataKey: "points",
      },
    ],
  };

  constructor(private globalService: GlobalService) {}

  get PlayerRankingUrl() {
    return "/game/" + AfterLoginRoutesEnum.PLAYER_RANKING;
  }
}
