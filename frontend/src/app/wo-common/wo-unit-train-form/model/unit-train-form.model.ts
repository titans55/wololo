import { Resources } from "src/app/pages/after-login/component/village/model/general/village-data.model";
import {
  VillageUnitType,
  // UnitDetails,
  UnitTypeConfig,
} from "../type/unit-types.type";

export class UnitTrainFormModel<T extends VillageUnitType> {
  public unitsToTrain: Array<UnitToTrain<keyof T>> = [];

  constructor(public villageId: number, unitsToTrain: T) {
    for (let unitName in unitsToTrain) {
      this.unitsToTrain.push({
        unitName: unitName,
        amount: 0,
      });
    }
  }

  // getRequiredResources<K extends { [key in keyof T]: UnitDetails }>(
  //   unitTypeConfig: K
  // ): Resources<number> {
  //   let totalWood = 0,
  //     totalClay = 0,
  //     totalIron = 0;
  //   this.unitsToTrain.forEach((unitToTrain) => {
  //     totalWood +=
  //       unitTypeConfig[unitToTrain.unitName].Cost.Wood * unitToTrain.amount;
  //     totalClay +=
  //       unitTypeConfig[unitToTrain.unitName].Cost.Clay * unitToTrain.amount;
  //     totalIron +=
  //       unitTypeConfig[unitToTrain.unitName].Cost.Iron * unitToTrain.amount;
  //   });
  //   return { wood: totalWood, iron: totalClay, clay: totalIron };
  // }

  //TODO change to typesafe like above
  getRequiredResources(unitTypeConfig: any): Resources<number> {
    let totalWood = 0,
      totalClay = 0,
      totalIron = 0;
    try {
      this.unitsToTrain.forEach((unitToTrain) => {
        totalWood +=
          unitTypeConfig[unitToTrain.unitName].Cost.Wood * unitToTrain.amount;
        totalClay +=
          unitTypeConfig[unitToTrain.unitName].Cost.Clay * unitToTrain.amount;
        totalIron +=
          unitTypeConfig[unitToTrain.unitName].Cost.Iron * unitToTrain.amount;
      });
    } catch {
      throw "only instances of UnitTypeConfig allowed as unitTypeConfig";
    }

    return { wood: totalWood, iron: totalClay, clay: totalIron };
  }

  getRequiredPopulation(unitTypeConfig: any): number {
    let requiredPopulation = 0;
    try {
      this.unitsToTrain.forEach((unitToTrain) => {
        requiredPopulation +=
          unitTypeConfig[unitToTrain.unitName].neededPopulation *
          unitToTrain.amount;
      });
    } catch {
      throw "only instances of UnitTypeConfig allowed as unitTypeConfig";
    }
    return requiredPopulation;
  }
}

export class UnitToTrain<T> {
  unitName: T;
  amount: number;
}
