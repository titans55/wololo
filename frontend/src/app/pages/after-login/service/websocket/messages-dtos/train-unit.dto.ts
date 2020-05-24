import { UnitNames } from "src/app/wo-common/wo-unit-train-form/type/unit-types.type";
import * as gameConfig from "../../../../../../../../gameConfig.json";

export type UnitTypeNames = keyof typeof gameConfig.units;

export interface TrainUnitDto {
  villageId: number;
  unitType: UnitTypeNames;
  unitName: UnitNames;
}
