import {
  ResourcesBuildings,
  Troops,
} from "../../../../pages/after-login/component/village/model/general/village.dto";

export class UnitTrainResponseDto {
  result: "Success" | "Fail";
  newResources: ResourcesBuildings;
  newTroops: Troops;
}
