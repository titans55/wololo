import * as moment from "moment";

export class UpgradingTimeModel {
  public label: string;
  constructor(public time: moment.Moment) {}
}
