import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";

@Component({
  selector: "wo-progress-bar",
  templateUrl: "./wo-progress-bar.component.html",
  styleUrls: ["./wo-progress-bar.component.css"],
})
export class WoProgressBarComponent implements OnInit {
  @Input() startTime: Date;
  @Input() endTime: Date;
  @Output() onProgresFinish: EventEmitter<void> = new EventEmitter();
  private percantage: number = 0;
  interval;

  constructor() {}

  ngOnInit() {
    if (new Date() > this.endTime) {
      this.percantage = 100;
    } else {
      const totalTimeDiffMs = this.endTime.getTime() - this.startTime.getTime();
      const elapsedTimeDiffMs = new Date().getTime() - this.startTime.getTime();
      this.percantage = parseInt(
        ((elapsedTimeDiffMs / totalTimeDiffMs) * 100).toFixed()
      );
      this.interval = setInterval(() => {
        if (this.percantage == 100) {
          clearInterval(this.interval);
          this.onProgresFinish.emit();
        } else {
          this.percantage += 1;
        }
      }, totalTimeDiffMs / 100);
    }
  }
}
