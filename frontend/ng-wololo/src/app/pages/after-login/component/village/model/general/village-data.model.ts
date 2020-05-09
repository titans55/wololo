import * as gameConfig from "../../../../../../../../../../wololo/game-config/gameConfig.json";
import { Subject, ReplaySubject } from "rxjs";
import {
  ResourcesBuildings,
  ResourceBuildingDetails,
  Upgrading,
  Village,
  SelectedVillageBuildings,
  Troops,
  Coords,
} from "./village.dto";
export type GameConfig = typeof gameConfig;
export type BuildingsConfigs = typeof gameConfig.buildings;
export type BuildingConfig =
  | typeof gameConfig.buildings
  | typeof gameConfig.buildings.resources;

export interface Resources<T> {
  wood: T;
  iron: T;
  clay: T;
}

export class VillageDataModel {
  buildings: BuildingModel[];
  units: UnitModel[];
  resources: ResourcesModel;
}

export class ResourcesModel implements Resources<ResourceModel> {
  wood: ResourceModel = new ResourceModel("wood");
  iron: ResourceModel = new ResourceModel("iron");
  clay: ResourceModel = new ResourceModel("clay");
}

export class ResourceModel implements ResourceBuildingDetails {
  private _buildingName: keyof ResourcesBuildings;
  currentSummary: ReplaySubject<
    VillageResourceDetailModel
  > = new ReplaySubject();
  level: number;
  sum: number;
  lastInteractionDate: Date;
  upgrading: Upgrading;

  constructor(public resourceName: string) {
    switch (resourceName) {
      case "wood":
        this._buildingName = "woodCamp";
        break;
      case "iron":
        this._buildingName = "ironMine";
        break;
      case "clay":
        this._buildingName = "clayPit";
        break;
    }
  }

  get buildingName(): string {
    return this._buildingName;
  }
}

export class UnitModel {}

export class BuildingModel {
  name: string;
  level: BuildingLevels;
}

export class ResourceBuildingModel extends BuildingModel {}

export type BuildingLevels = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

export class VillageResourceDetailModel {
  quantity: number;
  isCapacityReached: boolean;
}

export class PopulationModel {
  constructor(
    public currentPopulation: number,
    public populationLimit: number
  ) {}
}

export class VillageModel implements Village {
  buildings: SelectedVillageBuildings;
  villageName: string;
  troops: Troops;
  villageId: number;
  coords: Coords;
  selected: boolean = false;
}
