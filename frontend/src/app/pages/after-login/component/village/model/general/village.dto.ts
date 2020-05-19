import { Resources } from "./village-data.model";

export interface PlayerDataDto {
  totalIncomingStrangerTroops: any[];
  totalOnMove: any[];
  villagesInfo: Village[];
  selectedVillage: Village;
  gameConfig: GameConfig;
  unviewedReportExists: boolean;
  page: string;
}

export interface GameConfig {
  buildings: GameConfigBuildings;
  units: Units;
}

export interface GameConfigBuildings {
  townCenter: Building;
  resources: ResourcesBuildings;
  storage: Building;
  farm: Farm;
  barracks: Building;
  stable: Building;
  workshop: Building;
}

export interface Building {
  trainingSpeed?: { [key: string]: number };
  upgradeTime: { [key: string]: number };
  neededPopulation: { [key: string]: number };
  upgradingCosts: { [key: string]: Resources<number> };
  pointByLevel: { [key: string]: number };
  hourlyProductionByLevel?: { [key: string]: number };
  capacity?: { [key: string]: number };
  buildingSpeed?: { [key: string]: number };
}

export interface Farm {
  populationLimit: { [key: string]: number };
  upgradeTime: { [key: string]: number };
  upgradingCosts: { [key: string]: Resources<number> };
  pointByLevel: { [key: string]: number };
}

export interface Units {
  infantry: UnitsInfantry;
  cavalry: UnitsCavalry;
  siegeWeapons: UnitsSiegeWeapons;
  folkHero: FolkHero;
}

export interface UnitsCavalry {
  scout: Scout;
  lightCavalry: HeavyCavalry;
  heavyCavalry: HeavyCavalry;
}

export interface HeavyCavalry {
  cost: Resources<number>;
  skills: HeavyCavalrySkills;
  neededPopulation: number;
  neededTrainingBaseTime: number;
  speed: number;
  neededBuildings?: NeededBuildings;
}

export interface NeededBuildings {
  barracks: NeededBuildingsBarracks;
}

export interface NeededBuildingsBarracks {
  level: number;
}

export interface HeavyCavalrySkills {
  attack: number;
  defence: number;
  cavalryDefence: number;
  wallAttack?: number;
}

export interface Scout {
  cost: Resources<number>;
  skills: ScoutSkills;
  neededPopulation: number;
  neededTrainingBaseTime: number;
  speed: number;
}

export interface ScoutSkills {
  scoutingAttack: number;
  scoutingDefence: number;
  attack: number;
  defence: number;
  cavalryDefence: number;
}

export interface FolkHero {}

export interface UnitsInfantry {
  spearman: HeavyCavalry;
  swordsman: HeavyCavalry;
  axeman: HeavyCavalry;
  archer: HeavyCavalry;
}

export interface UnitsSiegeWeapons {
  ram: RAM;
  catapult: Catapult;
}

export interface Catapult {
  cost: Resources<number>;
  skills: CatapultSkills;
  neededPopulation: number;
  neededTrainingBaseTime: number;
  speed: number;
}

export interface CatapultSkills {
  wallAttack: number;
  buildingAttack: number;
  attack: number;
  defence: number;
  cavalryDefence: number;
}

export interface RAM {
  cost: Resources<number>;
  skills: HeavyCavalrySkills;
  neededPopulation: number;
  neededTrainingBaseTime: number;
  speed: number;
}

export interface Village {
  buildings: SelectedVillageBuildings;
  villageName: string;
  troops: Troops;
  villageId: number;
  coords: Coords;
}

export interface SelectedVillageBuildings {
  resources: ResourcesBuildings;
  barracks: BaseBuilding;
  workshop: BaseBuilding;
  stable: BaseBuilding;
  farm: BaseBuilding;
  storage: BaseBuilding;
  townCenter: BaseBuilding;
}

export interface BaseBuilding {
  level: number;
  upgrading: Upgrading;
}

export interface Upgrading {
  state: boolean;
  taskId: string;
  time: Time;
}

export class Time {
  startedUpgradingAt: Date;
  willBeUpgradedAt: Date;
}

export interface ResourcesBuildings {
  clayPit: ResourceBuildingDetails;
  ironMine: ResourceBuildingDetails;
  woodCamp: ResourceBuildingDetails;
}

export interface ResourceBuildingDetails extends BaseBuilding {
  sum: number;
  lastInteractionDate: Date;
}

export interface Coords {
  x: number;
  y: number;
}

export interface Troops {
  inVillage: InVillage;
  total: InVillage;
  incomingStrangerTroops: FolkHero;
  onMove: FolkHero;
  trainingQueue: TrainingQueue;
}

export interface InVillage {
  cavalry: InVillageCavalry;
  infantry: InVillageInfantry;
  siegeWeapons: InVillageSiegeWeapons;
}

export interface InVillageCavalry {
  scout: number;
  heavyCavalry: number;
  lightCavalry: number;
}

export interface InVillageInfantry {
  archer: number;
  axeman: number;
  spearman: number;
  swordsman: number;
}

export interface InVillageSiegeWeapons {
  ram: number;
  catapult: number;
}

export interface TrainingQueue {
  infantry: any[];
  cavalry: any[];
  siegeWeapons: any[];
  other: any[];
}
