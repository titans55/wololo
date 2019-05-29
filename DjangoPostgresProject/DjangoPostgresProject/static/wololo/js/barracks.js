"use strict";
var village_id
var gameConfigs = JSON.parse(($("#gameConfigData").attr("data")).replace(/'/g, '"'))
var villageData = JSON.parse(($("#villageDataJSON").attr("data")).replace(/'/g, '"'))
$(function(){
    village_id = villageData.id
    displayNeededTimeForInfantryUnits()
})

function displayNeededTimeForInfantryUnits(){
    for(let [unitName, units] of Object.entries(gameConfigs.units.infantry)){
        units.neededTrainingBaseTime
        
    };

    $(".neededTime").each(function(){
        const unitName = $(this).attr("unitName");
        const baseTrainingTime = gameConfigs.units.infantry[unitName].neededTrainingBaseTime
        const barracksLevel = villageData.barracks.level
        const speedPercantageOfBarracks = gameConfigs.buildings.barracks.trainingSpeed[barracksLevel]
        const neededTrainingTime = calculateTimeFromMinutes(lowerByPercantage(baseTrainingTime, speedPercantageOfBarracks))
        $(this).html(neededTrainingTime)
    })
}