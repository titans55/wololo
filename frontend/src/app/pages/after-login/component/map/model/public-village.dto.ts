import { Coords } from "../../village/model/general/village.dto";

export interface PublicVillageDto {
  userId: number;
  villageId: number;
  coords: Coords;
  villageName: string;
  playerName: string;
  points: number;
  owner?: boolean;
}
