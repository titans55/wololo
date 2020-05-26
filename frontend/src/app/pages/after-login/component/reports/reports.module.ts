import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { ReportsComponent } from "./reports/reports.component";
import { WoCommonModule } from "src/app/wo-common/wo-common.module";
import { ReportComponent } from "./report/report.component";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [ReportsComponent, ReportComponent],
})
export class ReportsModule {}
