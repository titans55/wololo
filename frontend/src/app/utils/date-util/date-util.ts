import * as moment from "moment";

export function calculateHumanizedTimeFromMinutes(mins: number): string {
  let formattedStr: string = moment("2015-01-01")
    .startOf("day")
    .minutes(mins)
    .format("H:mm:ss");
  return formattedStr;
}
