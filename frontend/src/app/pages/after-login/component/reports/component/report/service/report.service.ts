import { Injectable } from "@angular/core";
import { GlobalService } from "src/app/pages/after-login/service/global.service";

@Injectable()
export class ReportService {
  constructor(private globalService: GlobalService) {}

  updateReportToViewed(reportId: number): Promise<any> {
    return this.globalService.post("report-viewed/" + reportId.toString());
  }

  getReportById(reportId: number): Promise<any> {
    return this.globalService.get("reports/?id=" + reportId);
  }
}
