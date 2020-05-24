import { Component, OnInit, Input, Output, EventEmitter } from "@angular/core";
import { UnitTypeConfig, VillageUnitType } from "../type/unit-types.type";
import {
  UnitTrainFormModel,
  UnitToTrain,
} from "../model/unit-train-form.model";
import { ToastrService } from "ngx-toastr";
import { VillageResourcesService } from "src/app/pages/after-login/partials/component/village-resources/service/village-resources.service";
import { Subscription } from "rxjs";
import {
  VillageResourceDetailModel,
  PopulationModel,
} from "src/app/pages/after-login/component/village/model/general/village-data.model";
import { WoUnitTrainService } from "../service/wo-unit-train.service";

@Component({
  selector: "wo-unit-train-form",
  templateUrl: "./wo-unit-train-form.component.html",
  styleUrls: ["./wo-unit-train-form.component.css"],
})
export class WoUnitTrainFormComponent implements OnInit {
  @Input() villageId: number;
  @Input() unitTypeConfig: UnitTypeConfig;
  @Input() inVillageUnits: VillageUnitType;
  @Input() totalUnits: VillageUnitType;
  @Input() trainUrl: string;

  form: UnitTrainFormModel<VillageUnitType>;
  subscriptions: Subscription = new Subscription();
  currentWood: VillageResourceDetailModel;
  currentIron: VillageResourceDetailModel;
  currentClay: VillageResourceDetailModel;
  populationInfo: PopulationModel;

  constructor(
    private toastr: ToastrService,
    private villageResourcesService: VillageResourcesService,
    private woUnitTrainService: WoUnitTrainService
  ) {}

  ngOnInit() {
    this.initUnitTrainForm();
    console.log(this.form);

    this.subscriptions.add(
      this.villageResourcesService.wood.currentSummary.subscribe(
        (currentWood) => {
          this.currentWood = currentWood;
        }
      )
    );
    this.subscriptions.add(
      this.villageResourcesService.iron.currentSummary.subscribe(
        (currentIron) => {
          this.currentIron = currentIron;
        }
      )
    );
    this.subscriptions.add(
      this.villageResourcesService.clay.currentSummary.subscribe(
        (currentClay) => {
          this.currentClay = currentClay;
        }
      )
    );
    this.subscriptions.add(
      this.villageResourcesService.populationSubject.subscribe(
        (populationInfo) => {
          this.populationInfo = populationInfo;
        }
      )
    );
  }

  onTrainClick(): void {
    if (!this.hasResources()) {
      this.toastr.error("Unsufficient resources!");
      return;
    }
    if (!this.hasPopulation()) {
      this.toastr.error("Exceeds population limit!");
      return;
    }
    this.woUnitTrainService.train(this.trainUrl, this.form).then(() => {
      this.initUnitTrainForm();
    });
  }

  hasResources(): boolean {
    let resources = this.form.getRequiredResources(this.unitTypeConfig);
    return (
      resources.wood <= this.currentWood.quantity &&
      resources.iron <= this.currentIron.quantity &&
      resources.clay <= this.currentClay.quantity
    );
  }

  hasPopulation(): boolean {
    let requiredPopulation = this.form.getRequiredPopulation(
      this.unitTypeConfig
    );
    return (
      requiredPopulation <=
      this.populationInfo.populationLimit -
        this.populationInfo.currentPopulation
    );
  }

  getNeededResourcesOrPopulationToDisplay(
    neededResourceOrPopulationPerUnit: number,
    numberOfUnits: number
  ): number {
    if (numberOfUnits > 1) {
      return neededResourceOrPopulationPerUnit * numberOfUnits;
    } else {
      return neededResourceOrPopulationPerUnit;
    }
  }

  private initUnitTrainForm(): void {
    this.form = new UnitTrainFormModel(this.villageId, this.inVillageUnits);
  }
}
