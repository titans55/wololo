import { Component, OnInit } from "@angular/core";
import { ReportsService } from "./service/reports.service";
import { DataSourceConfigs } from "src/app/wo-common/wo-datagrid/service/wo-datagrid.service";
import { GlobalService } from "src/app/pages/after-login/service/global.service";
import { UserService } from "src/app/pages/after-login/service/user/user.service";
import { Router } from "@angular/router";

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
        // includeHrefConfigs: {
        //   enabled: true,
        //   redirectionUrl: "game/reports",
        //   parameterColumn: "id",
        // },
        isHidden: true,
      },
      {
        dataKey: "isViewed",
        dataType: "boolean",
        isHidden: true,
      },
      {
        dataKey: "type",
        caption: "Report Type",
        customCellTemplateEnabled: true,
      },
      {
        dataKey: "content",
        caption: "Info",
        customCellTemplateEnabled: true,
      },
      {
        dataKey: "createdAt",
        dataType: "datetime",
      },
      {
        dataKey: "detailsButton",
        caption: "",
        customCellTemplateEnabled: true,
      },
    ],
  };
  userId: number;

  constructor(
    private globalService: GlobalService,
    private userService: UserService,
    private router: Router
  ) {}

  ngOnInit() {
    this.userId = this.userService.userId;
  }

  redirectToReportDetail(reportId: number) {
    this.router.navigateByUrl("/game/reports/" + reportId);
  }
}
