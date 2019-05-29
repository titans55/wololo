"use strict";
var village_id
var gameConfigs = JSON.parse(($("#gameConfigData").attr("data")).replace(/'/g, '"'))
var villageData = JSON.parse(($("#villageDataJSON").attr("data")).replace(/'/g, '"'))

$(function(){
    // data = JSON.parse(data.replace(/'/g, '"'))
    village_id = villageData.id
    incrementOfResorcesByTime()
    calculatePopulationAndWrite()
})

function incrementOfResorcesByTime(){
    //console.log(gameConfigs.buildings.resources, villageData.resources)

    let woodDate = moment(villageData.resources.woodCamp.lastInteractionDate).format()
    let ironDate = moment(villageData.resources.ironMine.lastInteractionDate).format()
    let clayDate = moment(villageData.resources.clayPit.lastInteractionDate).format()

    let storageCapacity = gameConfigs.buildings.storage.capacity[villageData.storage.level]
    // console.log(woodDate)
    tick()
    setInterval(() => {
        tick()
    },1000)

    function tick(){
        let now = moment(new Date())
        let woodHours = (now.diff(woodDate) / (1000 * 60 * 60))
        let ironHours = (now.diff(ironDate) / (1000 * 60 * 60))
        let clayHours = (now.diff(clayDate) / (1000 * 60 * 60))
        let currentWood =( gameConfigs.buildings.resources.woodCamp.hourlyProductionByLevel[villageData.resources.woodCamp.level]*woodHours).toFixed()
        currentWood = parseInt(currentWood) + parseInt(villageData.resources.woodCamp.sum)
        checkCapacityAndWrite('#wood', currentWood, storageCapacity)

        let currentIron =( gameConfigs.buildings.resources.ironMine.hourlyProductionByLevel[villageData.resources.ironMine.level]*ironHours).toFixed()
        currentIron = parseInt(currentIron) + parseInt(villageData.resources.ironMine.sum)
        checkCapacityAndWrite('#iron', currentIron, storageCapacity)

        let currentClay =( gameConfigs.buildings.resources.clayPit.hourlyProductionByLevel[villageData.resources.clayPit.level]*clayHours).toFixed()
        currentClay = parseInt(currentClay) + parseInt(villageData.resources.clayPit.sum)
        checkCapacityAndWrite('#clay', currentClay, storageCapacity)
    }

    $("#storage").html(gameConfigs.buildings.storage.capacity[villageData.storage.level])
}

function checkCapacityAndWrite(resourceHtmlID, currentAmount, storageLimit){

    if(currentAmount > storageLimit){
        $(resourceHtmlID).html(storageLimit)
        if (!$(resourceHtmlID).hasClass("text-danger")) {
            $(resourceHtmlID).addClass("text-danger");
        }
    }else{
        $(resourceHtmlID).html(currentAmount)
        if($(resourceHtmlID).hasClass("text-danger")){
            $(resourceHtmlID).removeClass("text-danger")
        }
    }
}
function calculatePopulationAndWrite(){
    let farmLimit = gameConfigs.buildings.farm.populationLimit[villageData.farm.level]
    let usedPopulation = 0
    $(".building").each(function(){
        let buildingName = $(this).attr("buildingName")
        if(buildingName!='farm'){
            let neededPopForEachBuilding = gameConfigs.buildings[buildingName].neededPopulation[villageData[buildingName].level]
            usedPopulation += neededPopForEachBuilding
        }
    })
    $(".resources").each(function(){
        let resourceBuildingName = $(this).attr("resourceBuildingName")
        // let reseourceType = $(this).attr("reseourceType")
        let neededPopForEachBuilding = gameConfigs.buildings.resources[resourceBuildingName].neededPopulation[villageData.resources[resourceBuildingName].level]
        usedPopulation += neededPopForEachBuilding
    })
   
    for(let [unitType, units] of Object.entries(villageData.troops.total)){
        for(let [unit, unitSize] of Object.entries(units)){
            usedPopulation += unitSize*gameConfigs.units[unitType][unit].neededPopulation
        }
    }
    
    console.log(usedPopulation,"wololo")
    $("#population").html(usedPopulation + " / " + farmLimit)
}