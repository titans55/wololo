import { Component, Input } from "@angular/core";
import { TrainingQueueElement } from "src/app/pages/after-login/component/village/model/general/village.dto";

@Component({
  selector: "wo-training-queue",
  templateUrl: "./wo-training-queue.component.html",
  styleUrls: ["./wo-training-queue.component.css"],
})
export class WoTrainingQueueComponent {
  @Input() trainingQueue: Array<TrainingQueueElement> = [];

  constructor() {}
}
