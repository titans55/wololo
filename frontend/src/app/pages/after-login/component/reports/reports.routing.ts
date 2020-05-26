import { Routes, RouterModule } from "@angular/router";
import { ReportsRoutesEnum } from "./enum/reports-routes.enum";
import { ReportsComponent } from "./component/reports/reports.component";
import { ReportComponent } from "./component/report/report.component";

export const ReportsRoutes: Routes = [
  {
    path: "",
    component: ReportsComponent,
  },
  {
    path: ":" + ReportsRoutesEnum.REPORT_INDEX_URL_PARAM,
    component: ReportComponent,
  },
];

export const ReportsRoute = RouterModule.forChild(ReportsRoutes);
