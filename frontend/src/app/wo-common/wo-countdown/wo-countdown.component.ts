import {
  Component,
  Input,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  OnDestroy,
} from "@angular/core";
@Component({
  selector: "wo-countdown",
  template: "{{ timeLeftStr }}",
})
export class WoCountdownComponent implements OnDestroy {
  private _date: Date;
  private _timing: number = 1000;
  private _interval;

  @Input()
  public set time(date: Date) {
    this._date = date;
    this.initCountdown();
  }

  @Input()
  public set timing(value: string | number) {
    this._timing = parseInt(value as string, 10);
    this.initCountdown();
  }

  constructor(private _changeDetector: ChangeDetectorRef) {}

  ngOnDestroy() {
    this._stopTimer();
  }

  private _stopTimer() {
    clearInterval(this._interval);
    this._interval = undefined;
  }

  private initCountdown() {
    setInterval(() => {
      if (this.timeLeftStr == "00:00:00") {
        this._stopTimer();
      } else {
        if (!this._changeDetector["destroyed"])
          this._changeDetector.detectChanges();
      }
    }, this._timing);
  }

  get timeLeftStr(): string {
    let now = new Date();
    let secondsDiff: number = (<any>new Date(this._date) - <any>now) / 1000;
    if (secondsDiff < 0) {
      return "00:00:00";
    }
    let hoursStr: string = Math.floor((secondsDiff / 60 / 24) % 24).toString();
    let minutesStr: string = Math.floor((secondsDiff / 60) % 60).toString();
    let secondsStr: string = Math.floor(secondsDiff % 60).toString();

    return (
      this.startWithZero(hoursStr) +
      ":" +
      this.startWithZero(minutesStr) +
      ":" +
      this.startWithZero(secondsStr)
    );
  }

  private startWithZero(digits: string): string {
    return digits.length > 1 ? digits : "0" + digits[0];
  }
}
