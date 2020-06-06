import { VillageProfileInfoDto } from "../../village-profile/dto/village-profile-info.dto";

export interface PlayerProfileDto {
  clan: string;
  points: number;
  regionSelected: boolean;
  userId: number;
  playersVillages: VillageProfileInfoDto[];
  username: string;
}
