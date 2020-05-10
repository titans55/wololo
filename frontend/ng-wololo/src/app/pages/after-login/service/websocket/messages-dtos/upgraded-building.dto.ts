import { SelectedVillageBuildings } from "../../../component/village/model/general/village.dto";

export interface UpgradedBuildingMessage {
  messageType: string;
  target: string;
  newBuildings: SelectedVillageBuildings;
  villageId: number;
}
