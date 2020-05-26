import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { ReplaySubject } from "rxjs";

export class DatagridColumn {
  dataKey: string;
  dataType?: "datetime" | "string" | "boolean" = "string";
  caption?: string;
  includeHrefConfigs?: IncludeHrefConfigs;
}

class IncludeHrefConfigs {
  enabled: boolean = false;
  redirectionUrl?: string;
  parameterColumn?: string;
}

export interface DataSourceConfigs {
  endpoint: string;
  httpOptions: Object;
  columns: Array<DatagridColumn>;
}

export class WoDataSource {
  count: number;
  next?: string;
  previous?: string;
  results: Array<any>;
  paginateBy: number;
  currentPageNumber: number;
}

@Injectable()
export class WoDatagridService {
  private _dataSource: WoDataSource;
  public dataSource: ReplaySubject<WoDataSource> = new ReplaySubject(1);
  private configs: DataSourceConfigs;

  constructor(public http: HttpClient) {}

  fetchDataSource(
    configs: DataSourceConfigs,
    paginatedUrl?: string
  ): Promise<void> {
    if (this.configs == null) this.setConfigs(configs);
    return this.http
      .get(
        paginatedUrl ? paginatedUrl : this.configs.endpoint,
        this.configs.httpOptions
      )
      .toPromise()
      .then((dataSource: WoDataSource) => {
        this._dataSource = dataSource;
        this.nextDataSource();
      });
  }

  private nextDataSource(): void {
    this.dataSource.next(this._dataSource);
  }

  private setConfigs(configs: DataSourceConfigs): void {
    this.configs = configs;
  }

  paginationButtonClicked(nextOrPrev: "next" | "prev"): void {
    this.fetchDataSource(
      this.configs,
      nextOrPrev == "next" ? this._dataSource.next : this._dataSource.previous
    );
  }
}
