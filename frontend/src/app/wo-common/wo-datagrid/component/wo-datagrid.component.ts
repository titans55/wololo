import { Component, OnInit, Input, OnDestroy } from "@angular/core";
import {
  WoDatagridService,
  DataSourceConfigs,
  WoDataSource,
} from "../service/wo-datagrid.service";
import { Subscription } from "rxjs";

@Component({
  selector: "wo-datagrid",
  templateUrl: "./wo-datagrid.component.html",
  styleUrls: ["./wo-datagrid.component.css"],
})
export class WoDatagridComponent implements OnInit, OnDestroy {
  @Input() dataSourceConfigs: DataSourceConfigs;

  private dataSourceSubscription: Subscription;
  public dataSource: WoDataSource;

  constructor(private service: WoDatagridService) {}

  ngOnInit() {
    this.service.fetchDataSource(this.dataSourceConfigs);
    this.dataSourceSubscription = this.service.dataSource.subscribe(
      (dataSource) => {
        this.dataSource = dataSource;
      }
    );
  }

  ngOnDestroy() {
    this.dataSourceSubscription.unsubscribe();
  }

  get totalPages(): number {
    console.log(this.dataSource);
    if (this.dataSource.count <= this.dataSource.paginateBy) {
      return 1;
    }
    return Math.ceil(this.dataSource.count / this.dataSource.paginateBy);
  }
}
