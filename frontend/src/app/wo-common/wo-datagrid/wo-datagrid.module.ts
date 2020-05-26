import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { WoDatagridComponent } from "./component/wo-datagrid.component";
import { WoDatagridService } from "./service/wo-datagrid.service";
import { WoPipesModule } from "../pipe/wo-pipes.module";
import { RouterModule } from "@angular/router";
import { WoDatagridCellComponent } from "./component/wo-datagrid-cell/wo-datagrid-cell.component";

@NgModule({
  imports: [CommonModule, WoPipesModule, RouterModule],
  declarations: [WoDatagridComponent, WoDatagridCellComponent],
  exports: [WoDatagridComponent],
  providers: [WoDatagridService],
})
export class WoDatagridModule {}
