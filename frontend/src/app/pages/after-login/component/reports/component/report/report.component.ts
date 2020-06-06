import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { ReportsRoutesEnum } from "../../enum/reports-routes.enum";
import { ReportService } from "./service/report.service";
import * as gameConfig from "../../../../../../../../../gameConfig.json";
import { AfterLoginRoutesEnum } from "src/app/pages/after-login/enum/after-login-routes.enum";

@Component({
  selector: "wo-report",
  templateUrl: "./report.component.html",
  styleUrls: ["./report.component.css"],
})
export class ReportComponent implements OnInit {
  reportIndex: number;
  report;
  constructor(private route: ActivatedRoute, private service: ReportService) {}

  ngOnInit() {
    console.log(gameConfig);
    this.route.paramMap.subscribe(async (params) => {
      try {
        this.reportIndex = parseInt(
          params.get(ReportsRoutesEnum.REPORT_INDEX_URL_PARAM)
        );
        await this.service
          .getReportById(this.reportIndex)
          .then(async (reports) => {
            this.report = reports.results[0];
            console.log(this.report);
            if (!this.report.isViewed)
              await this.service.updateReportToViewed(this.reportIndex);
          });
      } catch {
        this.reportIndex = undefined;
      }
    });
  }

  get gameConfig() {
    return gameConfig[`default`];
  }

  get AfterLoginRoutesEnum() {
    return AfterLoginRoutesEnum;
  }
}
