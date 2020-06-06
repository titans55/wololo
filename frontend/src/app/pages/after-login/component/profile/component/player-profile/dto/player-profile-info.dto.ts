export interface PlayerProfileInfoDto {
  villageId: number;
  villageName: string;
  points: number;
  userId: number;
  playerName: string;
  clan: string;
  region: string;
  coords: Coords;
}

export interface Coords {
  x: number;
  y: number;
}
