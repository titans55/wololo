import { Injectable } from "@angular/core";
import * as moment from "moment";
import {
  ResourcesModel,
  ResourceModel,
  VillageResourceDetailModel,
  PopulationModel,
  VillageModel,
} from "src/app/pages/after-login/component/village/model/general/village-data.model";
import * as gameConfigs from "../../../../../../../../../gameConfig.json";
import { GlobalService } from "src/app/pages/after-login/service/global.service";
import {
  PlayerDataDto,
  ResourceBuildingDetails,
  SelectedVillageBuildings,
  ResourcesBuildings,
} from "src/app/pages/after-login/component/village/model/general/village.dto";
import { ReplaySubject, Observable } from "rxjs";
import { UserService } from "src/app/pages/after-login/service/user/user.service";

@Injectable({
  providedIn: "root",
})
export class VillageResourcesService extends ResourcesModel {
  readonly resources: Array<ResourceModel> = [this.wood, this.iron, this.clay];
  private productionIntervals: Array<any> = [];
  constructor(
    private globalService: GlobalService,
    private userService: UserService
  ) {
    super();
  }

  public async production(forceFetchData: boolean = false): Promise<void> {
    await this.initPlayer(forceFetchData);
    this.resources.forEach((resource) => {
      this.productionInterval(resource);
    });
  }

  public async switchVillage(villageIndex: number) {
    await this.fetchPlayerData(villageIndex).then((playerData) => {
      this.userService.setPlayerData(villageIndex, playerData);
    });
    this.production();
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

  private produce(resourceModel: ResourceModel): void {
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

  private async initPlayer(forceFetchData: boolean = false): Promise<void> {
    for (let i = 0; i < this.productionIntervals.length; i++) {
      clearInterval(this.productionIntervals[i]);
      this.productionIntervals.pop();
    }
    if (forceFetchData || this.userService.getPlayerData() == null) {
      await this.fetchPlayerData(
        this.userService.getSelectedVillageIndex()
      ).then((playerData: PlayerDataDto) => {
        this.userService.setPlayerData(
          this.userService.getSelectedVillageIndex(),
          playerData
        );
      });
    }
    this.initVillage();
  }

  private fetchPlayerData(villageIndex: number = 0): Promise<PlayerDataDto> {
    console.log("fetching player data");
    return this.globalService
      .get("villagesView/" + villageIndex)
      .then((villageData: PlayerDataDto) => {
        return villageData;
      });
  }

  private initVillage() {
    this.setAndEmitStorageCapacity();
    this.setAndEmitPopulationInfo();
    this.setAndEmitVillagesOfPlayer();
    for (const resourceBuildingName in this.userService.getPlayerData()
      .selectedVillage.buildings.resources) {
      let resourceBuildingDetails: ResourceBuildingDetails = this.userService.getPlayerData()
        .selectedVillage.buildings.resources[resourceBuildingName];
      let resourceModel = this.resources.find((resource) => {
        return resource.buildingName == resourceBuildingName;
      });
      Object.assign(resourceModel, resourceBuildingDetails);
    }
  }

  private storageCapacity: number;
  storageSubject: ReplaySubject<number> = new ReplaySubject(1);
  private setAndEmitStorageCapacity(): void {
    this.storageCapacity =
      gameConfigs.buildings.storage.capacity[
        this.userService.getPlayerData().selectedVillage.buildings.storage.level
      ];
    return this.storageSubject.next(this.storageCapacity);
  }

  private population: PopulationModel;
  populationSubject: ReplaySubject<PopulationModel> = new ReplaySubject(1);
  private setAndEmitPopulationInfo() {
    let populationLimit: number =
      gameConfigs.buildings.farm.populationLimit[
        this.userService.getPlayerData().selectedVillage.buildings.farm.level
      ];
    this.userService.getPlayerData().selectedVillage.troops.total;
    this.population = new PopulationModel(
      this.calculateUsedPopulation(),
      populationLimit
    );
    this.populationSubject.next(this.population);
  }

  private villagesOfPlayer: Array<VillageModel>;
  private _villagesOfPlayerSubject: ReplaySubject<
    Array<VillageModel>
  > = new ReplaySubject(1);
  get villagesOfPlayerSubject(): Observable<VillageModel[]> {
    return this._villagesOfPlayerSubject.asObservable();
  }
  private setAndEmitVillagesOfPlayer() {
    console.log("emitting villages of players");
    this.villagesOfPlayer = [];
    this.userService.getPlayerData().villagesInfo.forEach((village) => {
      let villageModel = new VillageModel();
      Object.assign(villageModel, village);
      this.villagesOfPlayer.push(villageModel);
    });
    this.villagesOfPlayer.find((village) => {
      return (
        village.villageId ==
        this.userService.getPlayerData().selectedVillage.villageId
      );
    }).selected = true;
    this._villagesOfPlayerSubject.next(this.villagesOfPlayer);
  }

  private calculateUsedPopulation(): number {
    let usedPopulation = 0;

    for (const bn in this.userService.getPlayerData().selectedVillage
      .buildings) {
      const buildingName = <keyof SelectedVillageBuildings>bn;
      if (buildingName != "resources") {
        let level: number = this.userService.getPlayerData().selectedVillage
          .buildings[buildingName].level;
        usedPopulation +=
          gameConfigs.buildings[buildingName].neededPopulation[level];
      } else {
        for (const rbn in this.userService.getPlayerData().selectedVillage
          .buildings[buildingName]) {
          let resourceBuildingName = <keyof ResourcesBuildings>rbn;
          let level: number = this.userService.getPlayerData().selectedVillage
            .buildings[buildingName][resourceBuildingName].level;
          usedPopulation +=
            gameConfigs.buildings[buildingName][resourceBuildingName]
              .neededPopulation[level];
        }
      }
    }
    for (let [unitType, units] of Object.entries(
      this.userService.getPlayerData().selectedVillage.troops.total
    )) {
      for (let [unit, size] of Object.entries(units)) {
        const unitSize = <number>size;
        usedPopulation +=
          unitSize * gameConfigs.units[unitType][unit].neededPopulation;
      }
    }

    for (let [unitTypeName, unitTypeQueueList] of Object.entries(
      this.userService.getPlayerData().selectedVillage.troops.trainingQueue
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
