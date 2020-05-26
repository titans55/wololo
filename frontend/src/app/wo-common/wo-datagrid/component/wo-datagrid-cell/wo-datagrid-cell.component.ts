import { Component, OnInit, Input } from "@angular/core";
import { DatagridColumn } from "../../service/wo-datagrid.service";

@Component({
  selector: "wo-datagrid-cell",
  templateUrl: "./wo-datagrid-cell.component.html",
  styleUrls: ["./wo-datagrid-cell.component.css"],
})
export class WoDatagridCellComponent implements OnInit {
  @Input() column: DatagridColumn;
  @Input() cellData: any;

  constructor() {}

  ngOnInit() {}
}
