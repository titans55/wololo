import {
  Village,
  SelectedVillageBuildings,
  Troops,
  Coords,
} from "src/app/pages/after-login/component/village/model/general/village.dto";

export class SelectedVillageModel implements Village {
  buildings: SelectedVillageBuildings;
  villageName: string;
  troops: Troops;
  villageId: number;
  coords: Coords;
  villageIndex: number;
}
