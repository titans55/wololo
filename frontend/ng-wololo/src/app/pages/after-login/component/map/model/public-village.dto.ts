export interface PublicVillageDto {
  userId: number;
  villageId: number;
  coords: Coords;
  villageName: string;
  playerName: string;
  points: number;
  owner?: boolean;
}

export interface Coords {
  x: number;
  y: number;
}
