import { Injectable } from "@angular/core";
import * as gameConfig from "../../../../../../../../../../postgreswololo/wololo/game-config/gameConfig.json";

@Injectable({
  providedIn: "root",
})
export class VillageService {
  public buildingsConfig: typeof gameConfig.buildings = gameConfig.buildings;

  constructor() {}
}
