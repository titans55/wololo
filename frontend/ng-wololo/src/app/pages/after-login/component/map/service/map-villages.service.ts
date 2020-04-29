import { Injectable } from "@angular/core";
import { AuthenticatedGlobalService } from "../../../service/authenticated-global.service";
import { MapConfigsEnum } from "../enum/map-configs.enum";
import { PublicVillageDto } from "../model/public-village.dto";

@Injectable({
  providedIn: "root",
})
export class MapVillagesService {
  constructor(public authenticatedGlobalService: AuthenticatedGlobalService) {}

  getMapVillages(): Promise<Array<PublicVillageDto>> {
    return this.authenticatedGlobalService.get(
      MapConfigsEnum.MAP_VILLAGES_ENDPOINT
    );
  }
}
