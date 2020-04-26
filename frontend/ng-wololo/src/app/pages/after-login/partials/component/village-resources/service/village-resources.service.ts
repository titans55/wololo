import { Injectable } from "@angular/core";
import * as moment from "moment";
import {
  ResourcesModel,
  ResourceModel,
  VillageResourceDetailModel,
  PopulationModel,
  VillageModel,
} from "src/app/pages/after-login/component/village/model/village-data.model";
import * as gameConfigs from "../../../../../../../../../../../postgreswololo/wololo/game-config/gameConfig.json";
import { AuthenticatedGlobalService } from "src/app/pages/after-login/service/authenticated-global.service";
import {
  PlayerDataDto,
  ResourceBuildingDetails,
  SelectedVillageBuildings,
  ResourcesBuildings,
  Village,
} from "src/app/pages/after-login/component/village/model/village.dto";
import { TimeInterval, Subject } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class VillageResourcesService extends ResourcesModel {
  readonly resources: Array<ResourceModel> = [this.wood, this.iron, this.clay];
  private villageData: PlayerDataDto;
  private productionIntervals: Array<any> = [];

  constructor(public authenticatedGlobalService: AuthenticatedGlobalService) {
    super();
    this.production();
  }

  private async production(): Promise<void> {
    if (this.villageData == null) {
      await this.setPlayerData();
    }
    this.resources.forEach((resource) => {
      this.productionInterval(resource);
    });
  }

  private productionInterval(resourceModel: ResourceModel): void {
    if (resourceModel) {
      this.produce(resourceModel);
      this.productionIntervals.push(
        setInterval(() => {
          this.produce(resourceModel);
        }, (60 / gameConfigs.buildings.resources.woodCamp.hourlyProductionByLevel[resourceModel.level]) * 60 * 1000)
      );
    } else {
      throw "villageResourceBuildingDetails cannot be null or undefined";
    }
  }

  produce(resourceModel: ResourceModel): void {
    const hourlyProduction =
      gameConfigs.buildings.resources.woodCamp.hourlyProductionByLevel[
        resourceModel.level
      ];
    let now = moment(new Date());
    let woodHours =
      now.diff(resourceModel.lastInteractionDate) / (1000 * 60 * 60);

    let currentResource: number = parseInt(
      (hourlyProduction * woodHours).toFixed()
    );

    currentResource += resourceModel.sum;
    resourceModel.currentSummary.next(this.fitIntoStorage(currentResource));
  }

  private fitIntoStorage(quantity: number): VillageResourceDetailModel {
    return {
      quantity:
        quantity > this.storageCapacity ? this.storageCapacity : quantity,
      isCapacityReached: quantity > this.storageCapacity,
    };
  }

  public async setPlayerData(villageIndex: number = 0) {
    this.productionIntervals.forEach((productionInterval) => {
      clearInterval(productionInterval);
    });
    return this.authenticatedGlobalService
      .get("villagesView/" + villageIndex)
      .then((villageData: PlayerDataDto) => {
        this.villageData = villageData;
        this.setAndEmitStorageCapacity();
        this.setAndEmitPopulationInfo();
        this.setAndEmitVillagesOfPlayer();
        for (const resourceBuildingName in this.villageData.selectedVillage
          .buildings.resources) {
          let resourceBuildingDetails: ResourceBuildingDetails = this
            .villageData.selectedVillage.buildings.resources[
            resourceBuildingName
          ];
          let resourceModel = this.resources.find((resource) => {
            return resource.buildingName == resourceBuildingName;
          });
          Object.assign(resourceModel, resourceBuildingDetails);
        }
      });
  }

  private storageCapacity: number;
  storageSubject: Subject<number> = new Subject();
  private setAndEmitStorageCapacity(): void {
    this.storageCapacity =
      gameConfigs.buildings.storage.capacity[
        this.villageData.selectedVillage.buildings.storage.level
      ];
    return this.storageSubject.next(this.storageCapacity);
  }

  private population: PopulationModel;
  populationSubject: Subject<PopulationModel> = new Subject();
  private setAndEmitPopulationInfo() {
    let populationLimit: number =
      gameConfigs.buildings.farm.populationLimit[
        this.villageData.selectedVillage.buildings.farm.level
      ];
    this.villageData.selectedVillage.troops.total;
    this.population = new PopulationModel(
      this.calculateUsedPopulation(),
      populationLimit
    );
    this.populationSubject.next(this.population);
  }

  private villagesOfPlayer: Array<VillageModel>;
  villagesOfPlayerSubject: Subject<Array<VillageModel>> = new Subject();
  private setAndEmitVillagesOfPlayer() {
    this.villagesOfPlayer = [];
    this.villageData.villagesInfo.forEach((village) => {
      let villageModel = new VillageModel();
      Object.assign(villageModel, village);
      this.villagesOfPlayer.push(villageModel);
    });
    this.villagesOfPlayer.find((village) => {
      return village.villageId == this.villageData.selectedVillage.villageId;
    }).selected = true;
    this.villagesOfPlayerSubject.next(this.villagesOfPlayer);
  }

  private calculateUsedPopulation(): number {
    let usedPopulation = 0;

    for (const bn in this.villageData.selectedVillage.buildings) {
      const buildingName = <keyof SelectedVillageBuildings>bn;
      if (buildingName != "resources") {
        let level: number = this.villageData.selectedVillage.buildings[
          buildingName
        ].level;
        usedPopulation +=
          gameConfigs.buildings[buildingName].neededPopulation[level];
      } else {
        for (const rbn in this.villageData.selectedVillage.buildings[
          buildingName
        ]) {
          let resourceBuildingName = <keyof ResourcesBuildings>rbn;
          let level: number = this.villageData.selectedVillage.buildings[
            buildingName
          ][resourceBuildingName].level;
          usedPopulation +=
            gameConfigs.buildings[buildingName][resourceBuildingName]
              .neededPopulation[level];
        }
      }
    }
    for (let [unitType, units] of Object.entries(
      this.villageData.selectedVillage.troops.total
    )) {
      for (let [unit, size] of Object.entries(units)) {
        const unitSize = <number>size;
        usedPopulation +=
          unitSize * gameConfigs.units[unitType][unit].neededPopulation;
      }
    }

    for (let [unitTypeName, unitTypeQueueList] of Object.entries(
      this.villageData.selectedVillage.troops.trainingQueue
    )) {
      for (let queue in unitTypeQueueList) {
        usedPopulation +=
          unitTypeQueueList[queue]["unitsLeft"] *
          gameConfigs.units[unitTypeName][unitTypeQueueList[queue]["unitName"]]
            .neededPopulation;
      }
    }

    return usedPopulation;
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
