import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { ReportsComponent } from "./component/reports/reports.component";
import { ReportComponent } from "./component/report/report.component";
import { ReportService } from "./component/report/service/report.service";
import { ReportsService } from "./component/reports/service/reports.service";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [ReportsComponent, ReportComponent],
  providers: [ReportsService, ReportService],
})
export class ReportsModule {}
