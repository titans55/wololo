"use strict";
var village_id
var gameConfigs = JSON.parse(($("#gameConfigData").attr("data")).replace(/'/g, '"'))
var villageData = JSON.parse(($("#villageDataJSON").attr("data")).replace(/'/g, '"'))
$(function(){
    // data = JSON.parse(data.replace(/'/g, '"'))
    village_id = villageData.id
    initToggleVisualVillageSwitch()
    initVillage()
    console.log(villageData)
})

function initVillage(){
    initUpgradeButtons()
    displayNeededResourcesAndTimeForUpgrading()
    
}



function initUpgradeButtons(){



    let csrftoken = getCookie('csrftoken');
    
    $(".upgrade").on('click', function(){
        let now = new Date()
        let building_path = $(this).attr('id')
        $.ajax({
            type: 'POST',
            url: '/game/upgrade',
            data: {
                building_path: building_path,
                village_id: village_id,
                firingTime: now,
                csrfmiddlewaretoken: csrftoken 
            },
            success:function(data){

                if(data == 'Success'){
                    
                }else if(data == 'Fail'){
                    // alert("Fail")
                    console.log("WOLOLO")
                    $('#insufficentResources').modal('show')
                }
    
            }
        })
    });
}

function displayNeededResourcesAndTimeForUpgrading(){
    let speedPercantageOfTownCenter = gameConfigs.buildings.townCenter.buildingSpeed[villageData.townCenter.level]
    //upgrading costs
    $('.upgradeBuildings').each(function(){
        let buildingName = $(this).attr('buildingName')
        let buildingLevel = String(parseInt(villageData[String(buildingName)].level) + 1)
        let neededResources = gameConfigs.buildings[String(buildingName)].upgradingCosts[buildingLevel]
        let mins = gameConfigs.buildings[String(buildingName)].upgradeTime[buildingLevel]
        if(buildingName!='townCenter') mins = lowerByPercantage(mins, speedPercantageOfTownCenter)
        let neededTime = calculateTimeFromMinutes(mins)
        $(this).find(".neededWood").html(neededResources.wood)
        $(this).find(".neededIron").html(neededResources.iron)
        $(this).find(".neededClay").html(neededResources.clay)
        $(this).find(".neededTime").html(neededTime)
    })
    $('.upgradeResources').each(function(){
        let resourceBuilding = $(this).attr('buildingName')
        // let resourceType = $(this).attr('resourceType')
        let buildingLevel = String(parseInt(villageData.resources[String(resourceBuilding)].level) + 1)
        let neededResources = gameConfigs.buildings.resources[String(resourceBuilding)].upgradingCosts[buildingLevel]
        let mins = gameConfigs.buildings.resources[String(resourceBuilding)].upgradeTime[buildingLevel]
        mins = lowerByPercantage(mins, speedPercantageOfTownCenter)
        let neededTime = calculateTimeFromMinutes(mins)
        $(this).find(".neededWood").html(neededResources.wood)
        $(this).find(".neededIron").html(neededResources.iron)
        $(this).find(".neededClay").html(neededResources.clay)
        $(this).find(".neededTime").html(neededTime)
    })

    //upgrading times

}


function initSwitchVillageDropdownButton(){
    // $("#switchVillage")
}

function initToggleVisualVillageSwitch(){
    let textBasedVillageContent = $(".village-content").html()
    $("#toggleVisualVillage").val('off')

    $(".toggleVisualVillage").on("change",function(){
        ($("#toggleVisualVillage").val() == 'on' ? $("#toggleVisualVillage").val('off')   : $("#toggleVisualVillage").val('on') )
        console.log($("#toggleVisualVillage").val())

        if($("#toggleVisualVillage").val() == 'on'){
            const string = '<div class="row mt-5 mb-5"><div class="col"></div><div class="col"><h5>COMING SOON!</h5></div><div class="col"></div></div>'
            $(".village-content").html(string)
        }else{
            $(".village-content").html(textBasedVillageContent)
            initVillage()
        }
    })
}