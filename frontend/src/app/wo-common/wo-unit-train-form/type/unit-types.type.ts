import * as gameConfig from "../../../../../../gameConfig.json";
import {
  InVillageInfantry,
  InVillageCavalry,
  InVillageSiegeWeapons,
} from "src/app/pages/after-login/component/village/model/general/village.dto";

export type InfantryConfigs = typeof gameConfig.units.infantry;
export type CavalryConfigs = typeof gameConfig.units.cavalry;
export type SiegeWeaponsConfigs = typeof gameConfig.units.siegeWeapons;

export type UnitTypeConfig =
  | InfantryConfigs
  | CavalryConfigs
  | SiegeWeaponsConfigs;

export type VillageUnitType =
  | InVillageInfantry
  | InVillageCavalry
  | InVillageSiegeWeapons;

// export type unitNames =
//   | keyof InVillageInfantry
//   | keyof InVillageCavalry
//   | keyof InVillageSiegeWeapons;

// type InfantryUnitDetails = typeof gameConfig.units.infantry[keyof InfantryConfigs];
// type CavalryUnitDetails = typeof gameConfig.units.cavalry[keyof CavalryConfigs];
// type SiegeWeaponsUnitDetails = typeof gameConfig.units.siegeWeapons[keyof SiegeWeaponsConfigs];
// export type UnitDetails =
//   | InfantryUnitDetails
//   | CavalryUnitDetails
//   | SiegeWeaponsUnitDetails;
