import { Injectable } from "@angular/core";
import * as gameConfigs from "../../../../../../../../wololo/game-config/gameConfig.json";
import { Enviroment } from "../enviroment";
import { UserService } from "../user/user.service";
import { UpgradedBuildingMessage } from "./messages-dtos/upgraded-building.dto";
import { VillageResourcesService } from "src/app/pages/after-login/partials/component/village-resources/service/village-resources.service";

@Injectable({
  providedIn: "root",
})
export class WebsocketService {
  socket: WebSocket;
  constructor(
    private userService: UserService,
    private villageResourcesService: VillageResourcesService
  ) {}

  initWebsockets() {
    if (this.socket == null) {
      const parentThis = this;
      this.socket = new WebSocket(
        "ws://" + Enviroment.HOST + "ws/game/?token=" + this.userService.token
      );

      this.socket.onopen = function (e) {
        console.log("websocket connected", e);
      };

      this.socket.onmessage = function (e) {
        console.log("message Arrived");
        const incomingJson = JSON.parse(e.data);
        parentThis.incomingMessageEndpoints(incomingJson);
      };

      this.socket.onerror = function (e) {
        console.log("errorrr", e);
      };

      this.socket.onclose = function (e) {
        console.error("Chat socket closed unexpectedly");
      };
    }
  }

  incomingMessageEndpoints(incomingJson) {
    console.log(incomingJson, "message has arrived");

    switch (incomingJson.messageType) {
      case "upgradeBuilding":
        this.listenUpgradeBuilding(incomingJson);
        break;
      case "trainUnit":
        // this.listenTrainUnit(incomingJson);
        break;
      default:
        alert("message arrived endpoint is not defined");
    }
  }
  /*
    Listening Upgrade Building Notifications
*/

  listenUpgradeBuilding(upgradedBuildingMessage: UpgradedBuildingMessage) {
    console.log(upgradedBuildingMessage);
    let selectedVillage = this.userService.getSelectedVillageInfo();
    if (selectedVillage.villageId == upgradedBuildingMessage.villageId) {
      this.userService.setBuildingsOfSelectedVillage(
        upgradedBuildingMessage.newBuildings
      );
      this.villageResourcesService.production();
    }
    // if (incomingJson.village_id == village_id) {
    //   villageData.buildings = incomingJson.newBuildings;
    //   this.incrementLevelOfBuilding(incomingJson.target);
    //   const htmlTarget = $("[id='" + incomingJson.target + "-level']");
    //   $("body").append(
    //     "<div id='" +
    //       incomingJson.target +
    //       "-popup', class='popup' style='display:none;'>+1</div>"
    //   );
    //   const popperObj = $("[id='" + incomingJson.target + "-popup']");
    //   const popper = new Popper(htmlTarget, popperObj, {
    //     placement: "right",
    //   });
    //   popperObj.show();
    //   setTimeout(function () {
    //     popperObj.remove();
    //   }, 3000);
    // }
  }
  //   incrementLevelOfBuilding(target) {
  //     let targetRow;
  //     let newLevel = this.getBuildingCurrentLevel(target);
  //     console.log("incrementing Level");
  //     if (target.includes(".")) {
  //       let targetBuildingName = target.split(".")[1];
  //       // villageData.buildings.resources[targetBuildingName].level = newLevel
  //       // villageData.buildings.resources[targetBuildingName].upgrading.state = 'false';
  //       if (page == "myVillages") {
  //         console.log("hololo");
  //         targetRow = $("#resources-" + targetBuildingName + "-row");
  //         targetRow.find(".buildingDetailsSection").html(getUpgReqHtml());
  //         fillUpgReq(target);
  //         targetRow.find(".level").html(newLevel);
  //         targetRow.find(".upgradeOrCancelBtn").html(getUpgBtnHtml(target));
  //         initUpgradeButtons();
  //       }
  //     } else {
  //       // villageData.buildings[target].level = newLevel
  //       // villageData.buildings[target].upgrading.state = 'false';
  //       if (page == "myVillages") {
  //         targetRow = $("#" + target + "-row");
  //         targetRow.find(".buildingDetailsSection").html(getUpgReqHtml());
  //         fillUpgReq(target);
  //         targetRow.find(".level").html(newLevel);
  //         targetRow.find(".upgradeOrCancelBtn").html(getUpgBtnHtml(target));
  //         initUpgradeButtons();
  //       }
  //     }
  //   }

  //   fillUpgReq(target) {
  //     let targetBuildingName, targetRow, neededResources, mins;
  //     let buildingNextLevel = String(
  //       parseInt(this.getBuildingCurrentLevel(target)) + 1
  //     );
  //     if (target.includes(".")) {
  //       targetBuildingName = target.split(".")[1];
  //       targetRow = $("#resources-" + targetBuildingName + "-row");
  //       neededResources =
  //         gameConfigs.buildings.resources[String(targetBuildingName)]
  //           .upgradingCosts[buildingNextLevel];
  //     } else {
  //       targetBuildingName = target;
  //       targetRow = $("#" + targetBuildingName + "-row");
  //       neededResources =
  //         gameConfigs.buildings[String(targetBuildingName)].upgradingCosts[
  //           buildingNextLevel
  //         ];
  //     }
  //     let neededTime = getBuildingUpgradingNeededTime(target);
  //     targetRow.find(".neededWood").html(neededResources.wood);
  //     targetRow.find(".neededIron").html(neededResources.iron);
  //     targetRow.find(".neededClay").html(neededResources.clay);
  //     targetRow.find(".neededTime").html(neededTime);
  //   }

  //   getBuildingUpgradingNeededTime(building_path) {
  //     let mins = getBuildingUpgradingMins(building_path);
  //     let neededTime = calculateTimeFromMinutes(mins);
  //     return neededTime;
  //   }

  //   getBuildingUpgradingMins(building_path) {
  //     let mins, targetBuildingName;
  //     let buildingLevel = String(
  //       parseInt(getBuildingCurrentLevel(building_path)) + 1
  //     );
  //     if (building_path.includes(".")) {
  //       targetBuildingName = building_path.split(".")[1];
  //       mins =
  //         gameConfigs.buildings.resources[String(targetBuildingName)].upgradeTime[
  //           buildingLevel
  //         ];
  //     } else {
  //       targetBuildingName = building_path;
  //       mins =
  //         gameConfigs.buildings[String(targetBuildingName)].upgradeTime[
  //           buildingLevel
  //         ];
  //     }
  //     let speedPercantageOfTownCenter =
  //       gameConfigs.buildings.townCenter.buildingSpeed[
  //         villageData.buildings.townCenter.level
  //       ];
  //     mins = lowerByPercantage(mins, speedPercantageOfTownCenter);

  //     return mins;
  //   }

  //   getBuildingCurrentLevel(building_path) {
  //     let buildingLevel, targetBuildingName;
  //     if (building_path.includes(".")) {
  //       targetBuildingName = building_path.split(".")[1];
  //       buildingLevel =
  //         villageData.buildings.resources[String(targetBuildingName)].level;
  //     } else {
  //       targetBuildingName = building_path;
  //       buildingLevel = villageData.buildings[String(targetBuildingName)].level;
  //     }
  //     return buildingLevel;
  //   }

  //   getUpgReqHtml() {
  //     const unfilledUpgradeRequirements =
  //       '<div class="col">' +
  //       '<div class="neededWood">XXX</div> Wood' +
  //       "</div>" +
  //       '<div class="col">' +
  //       '<div class="neededIron">XXX</div> Iron' +
  //       "</div>" +
  //       '<div class="col">' +
  //       '<div class="neededClay">XXX</div> Clay' +
  //       "</div>" +
  //       '<div class="col">' +
  //       '<div class="neededTime">XXX</div>' +
  //       "</div>";
  //     return unfilledUpgradeRequirements;
  //   }

  //   getUpgBtnHtml(target) {
  //     let upgradeBtn =
  //       '<button class="upgrade btn btn-primary" id="' +
  //       target +
  //       '">Upgrade</button>';
  //     return upgradeBtn;
  //   }

  //   initProgressBar(buildingName) {
  //     const experimentalDelay = 3000; // in milliseconds
  //     let now = moment(new Date());
  //     let buildingUpgrading;
  //     if (buildingName.includes(".")) {
  //       buildingName = buildingName.split(".")[1];
  //       buildingUpgrading =
  //         villageData.buildings.resources[String(buildingName)].upgrading;
  //     } else {
  //       buildingUpgrading = villageData.buildings[String(buildingName)].upgrading;
  //     }
  //     let startedUpgradingAt = moment(
  //       buildingUpgrading.time.startedUpgradingAt
  //     ).format();
  //     let willBeUpgradedAt = moment(
  //       buildingUpgrading.time.willBeUpgradedAt
  //     ).format();
  //     let totalUpgradingSeconds =
  //       (moment(willBeUpgradedAt).diff(moment(startedUpgradingAt)) +
  //         experimentalDelay) /
  //       1000; //seconds
  //     let timeDone = moment(now).diff(moment(startedUpgradingAt).format()) / 1000; //seconds
  //     let period = totalUpgradingSeconds / 100;
  //     let current_progress =
  //       parseInt(timeDone / period) >= 100 ? 100 : parseInt(timeDone / period);
  //     $("#" + buildingName + "-progressBar")
  //       .css("width", current_progress + "%")
  //       .attr("aria-valuenow", current_progress)
  //       .text(current_progress + "% Complete");
  //     if (current_progress != 100) {
  //       let interval = setInterval(function () {
  //         current_progress += 1;
  //         $("#" + buildingName + "-progressBar")
  //           .css("width", current_progress + "%")
  //           .attr("aria-valuenow", current_progress)
  //           .text(current_progress + "% Complete");
  //         if (current_progress >= 100) clearInterval(interval);
  //       }, period * 1000);
  //     }
  //   }

  //   getProgressBarHtml(building_path) {
  //     let buildingName;
  //     if (building_path.includes(".")) {
  //       buildingName = building_path.split(".")[1];
  //     } else {
  //       buildingName = building_path;
  //     }

  //     const progressBarHtml =
  //       '<div class="progress">' +
  //       '<div id="' +
  //       buildingName +
  //       '-progressBar" class="progress-bar progress-bar-success progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%">' +
  //       '<span id="current-progress">' +
  //       "</span>" +
  //       "</div>";

  //     return progressBarHtml;
  //   }

  //   getTargetBuildingRow(building_path) {
  //     let targetRow, targetBuildingName;
  //     if (building_path.includes(".")) {
  //       targetBuildingName = building_path.split(".")[1];
  //       targetRow = $("#resources-" + targetBuildingName + "-row");
  //     } else {
  //       targetBuildingName = building_path;
  //       targetRow = $("#" + targetBuildingName + "-row");
  //     }
  //     return targetRow;
  //   }

  //   /*
  //     Listening Upgrade Building Notifications Ends
  // */

  //   listenTrainUnit(incomingJson) {
  //     console.log(incomingJson);
  //     if (incomingJson.village_id == village_id) {
  //       // villageData.buildings = incomingJson.newBuildings
  //       if (page == "barracks") {
  //         let targetQueueElement = $(".queueElement").first();
  //         let oldUnitsLeft = parseInt(
  //           targetQueueElement.find(".unitsLeft").html().split(" ")[0]
  //         );
  //         let unitsLeft = oldUnitsLeft - 1;
  //         if (unitsLeft == 0) {
  //           targetQueueElement.remove();
  //         } else {
  //           targetQueueElement
  //             .find(".unitsLeft")
  //             .html(unitsLeft.toString() + " " + incomingJson.unit_name);
  //         }
  //       }
  //     }
  //   }
}
