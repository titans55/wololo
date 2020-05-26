import { Component, OnInit } from "@angular/core";
import { ReportsService } from "./service/reports.service";
import { DataSourceConfigs } from "src/app/wo-common/wo-datagrid/service/wo-datagrid.service";
import { GlobalService } from "src/app/pages/after-login/service/global.service";

@Component({
  selector: "wo-reports",
  templateUrl: "./reports.component.html",
  styleUrls: ["./reports.component.css"],
})
export class ReportsComponent implements OnInit {
  readonly dataSourceConfigs: DataSourceConfigs = {
    endpoint: this.globalService.getEndpointUrl("reports"),
    httpOptions: this.globalService.httpOptions,
    columns: [
      {
        dataKey: "id",
        includeHrefConfigs: {
          enabled: true,
          redirectionUrl: "game/reports",
          parameterColumn: "id",
        },
      },
      {
        dataKey: "type",
      },
      {
        dataKey: "isViewed",
        dataType: "boolean",
      },
      {
        dataKey: "createdAt",
        dataType: "datetime",
      },
    ],
  };

  constructor(private globalService: GlobalService) {}

  ngOnInit() {}
}
