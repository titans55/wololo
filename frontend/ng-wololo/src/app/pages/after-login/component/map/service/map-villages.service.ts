import { Injectable } from "@angular/core";
import { GlobalService } from "../../../service/global.service";
import { MapConfigsEnum } from "../enum/map-configs.enum";
import { PublicVillageDto } from "../model/public-village.dto";

@Injectable({
  providedIn: "root",
})
export class MapVillagesService {
  constructor(public globalService: GlobalService) {}

  getMapVillages(): Promise<Array<PublicVillageDto>> {
    return this.globalService.get(MapConfigsEnum.MAP_VILLAGES_ENDPOINT);
  }
}
