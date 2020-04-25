import { Injectable } from "@angular/core";
import * as moment from "moment";
import {
  ResourcesModel,
  ResourceModel,
} from "src/app/pages/after-login/component/village/model/village-data.model";
import * as gameConfigs from "../../../../../../../../../../../postgreswololo/wololo/game-config/gameConfig.json";

@Injectable({
  providedIn: "root",
})
export class VillageResourcesService extends ResourcesModel {
  readonly resources: Array<ResourceModel> = [this.wood, this.iron, this.clay];
  constructor() {
    super();
    this.production();
  }

  private production(): void {
    this.resources.forEach((resource) => {
      resource.buildingLevel = 10;
      resource.lastInteractionDate = new Date();
      resource.lastSummary = 0;
      this.productionInterval(resource);
    });
  }

  private productionInterval(resource: ResourceModel): void {
    this.produce(resource);
    setInterval(() => {
      this.produce(resource);
    }, (60 / gameConfigs.buildings.resources.woodCamp.hourlyProductionByLevel[resource.buildingLevel]) * 60 * 1000);
  }

  produce(resource: ResourceModel): void {
    const hourlyProduction =
      gameConfigs.buildings.resources.woodCamp.hourlyProductionByLevel[
        resource.buildingLevel
      ];
    let now = moment(new Date());
    let woodHours = now.diff(resource.lastInteractionDate) / (1000 * 60 * 60);

    let currentResource: number = parseInt(
      (hourlyProduction * woodHours).toFixed()
    );
    currentResource += resource.lastSummary;
    resource.currentSummary.next(currentResource);
  }

  // incrementOfResorcesByTime(){

  //   let woodDate = moment(villageData.buildings.resources.woodCamp.lastInteractionDate).format()
  //   let ironDate = moment(villageData.buildings.resources.ironMine.lastInteractionDate).format()
  //   let clayDate = moment(villageData.buildings.resources.clayPit.lastInteractionDate).format()

  //   let storageCapacity = gameConfigs.buildings.storage.capacity[villageData.buildings.storage.level]
  //   this.tick()
  //   setInterval(() => {
  //       this.tick()
  //   },1000)

  //   tick(){
  //       let now = moment(new Date())
  //       let woodHours = (now.diff(woodDate) / (1000 * 60 * 60))
  //       let ironHours = (now.diff(ironDate) / (1000 * 60 * 60))
  //       let clayHours = (now.diff(clayDate) / (1000 * 60 * 60))
  //       let currentWood =( gameConfigs.buildings.resources.woodCamp.hourlyProductionByLevel[villageData.buildings.resources.woodCamp.level]*woodHours).toFixed()
  //       currentWood = parseInt(currentWood) + parseInt(villageData.buildings.resources.woodCamp.sum)
  //       checkCapacityAndWrite('#wood', currentWood, storageCapacity)

  //       let currentIron =( gameConfigs.buildings.resources.ironMine.hourlyProductionByLevel[villageData.buildings.resources.ironMine.level]*ironHours).toFixed()
  //       currentIron = parseInt(currentIron) + parseInt(villageData.buildings.resources.ironMine.sum)
  //       checkCapacityAndWrite('#iron', currentIron, storageCapacity)

  //       let currentClay =( gameConfigs.buildings.resources.clayPit.hourlyProductionByLevel[villageData.buildings.resources.clayPit.level]*clayHours).toFixed()
  //       currentClay = parseInt(currentClay) + parseInt(villageData.buildings.resources.clayPit.sum)
  //       checkCapacityAndWrite('#clay', currentClay, storageCapacity)
  //   }

  //   $("#storage").html(gameConfigs.buildings.storage.capacity[villageData.buildings.storage.level])
  // }

  // checkCapacityAndWrite(resourceHtmlID, currentAmount, storageLimit){

  //   if(currentAmount > storageLimit){
  //       $(resourceHtmlID).html(storageLimit)
  //       if (!$(resourceHtmlID).hasClass("text-danger")) {
  //           $(resourceHtmlID).addClass("text-danger");
  //       }
  //   }else{
  //       $(resourceHtmlID).html(currentAmount)
  //       if($(resourceHtmlID).hasClass("text-danger")){
  //           $(resourceHtmlID).removeClass("text-danger")
  //       }
  //   }
  // }
  // calculatePopulationAndWrite(){
  //   let farmLimit = gameConfigs.buildings.farm.populationLimit[villageData.buildings.farm.level]
  //   let usedPopulation = 0
  //   $(".building").each(function(){
  //       let buildingName = $(this).attr("buildingName")
  //       if(buildingName!='farm'){
  //           let neededPopForEachBuilding = gameConfigs.buildings[buildingName].neededPopulation[villageData.buildings[buildingName].level]
  //           usedPopulation += neededPopForEachBuilding
  //       }
  //   })
  //   $(".resources").each(function(){
  //       let resourceBuildingName = $(this).attr("resourceBuildingName")
  //       // let reseourceType = $(this).attr("reseourceType")
  //       let neededPopForEachBuilding = gameConfigs.buildings.resources[resourceBuildingName].neededPopulation[villageData.buildings.resources[resourceBuildingName].level]
  //       usedPopulation += neededPopForEachBuilding
  //   })

  //   for(let [unitType, units] of Object.entries(villageData.troops.total)){
  //       for(let [unit, unitSize] of Object.entries(units)){
  //           usedPopulation += unitSize*gameConfigs.units[unitType][unit].neededPopulation
  //       }
  //   }

  //   for(let [unitTypeName, unitTypeQueueList] of Object.entries(villageData.troops.trainingQueue)){
  //       for(let queue in unitTypeQueueList){
  //           usedPopulation += unitTypeQueueList[queue]['unitsLeft']*gameConfigs.units[unitTypeName][unitTypeQueueList[queue]['unitName']].neededPopulation
  //       }
  //   }

  //   $("#population").html(usedPopulation + " / " + farmLimit)
  //   if(usedPopulation>=farmLimit){
  //       $("#population").addClass("text-danger")
  //   }
  // }
}
