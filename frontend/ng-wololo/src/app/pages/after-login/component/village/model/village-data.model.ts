import * as gameConfig from "../../../../../../../../../../postgreswololo/wololo/game-config/gameConfig.json";
import { Subject } from "rxjs";
export type GameConfig = typeof gameConfig;

export class VillageDataModel {
  buildings: BuildingModel[];
  units: UnitModel[];
  resources: ResourcesModel;
}

export class ResourcesModel {
  wood: ResourceModel = new ResourceModel();
  iron: ResourceModel = new ResourceModel();
  clay: ResourceModel = new ResourceModel();
}

export class ResourceModel {
  buildingLevel: BuildingLevels = 4;
  lastInteractionDate: Date = new Date();
  lastSummary: number = 0;
  currentSummary: Subject<number> = new Subject();
}

export class UnitModel {}

export class BuildingModel {
  name: string;
  level: BuildingLevels;
}

export class ResourceBuildingModel extends BuildingModel {}

export type BuildingLevels = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
