import { Coords } from "../../../../village/model/general/village.dto";

export interface VillageProfileInfoDto {
  villageId: number;
  villageName: string;
  points: number;
  userId: number;
  playerName: string;
  clan: string;
  region: string;
  coords: Coords;
}
