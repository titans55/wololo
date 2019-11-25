"use strict";
var gameConfigs = JSON.parse(($("#gameConfigData").attr("data")).replace(/'/g, '"'))
var villageData = JSON.parse(($("#villageDataJSON").attr("data")).replace(/'/g, '"'))
$(function(){
    // data = JSON.parse(data.replace(/'/g, '"'))
    initToggleVisualVillageSwitch()
    initVillage()
})

function initVillage(){
    initUpgradeButtons()
    initCancelButtons()
    displayNeededResourcesAndTimeForUpgrading()
}



function initUpgradeButtons(){

    let csrftoken = getCookie('csrftoken');

    $(".upgrade").each(function(){
        if(!$(this).data('click-init')){
            $(this).data('click-init', true)
            $(this).on('click', function(){
                let firingTime = new Date() //now
                let building_path = $(this).attr('id')
                $.ajax({
                    type: 'POST',
                    url: '/game/upgrade',
                    data: {
                        building_path: building_path,
                        village_id: villageData.village_id,
                        firingTime: firingTime,
                        csrfmiddlewaretoken: csrftoken 
                    },
                    success:function(data){
                        if(data['result'] == 'Success'){
                            console.log(data['newResources'])

                            if(!building_path.includes('.')){
                                villageData.buildings[building_path] = data['newBuilding']
                            }
                            console.log(data['newResources'])
                            villageData.buildings.resources = data['newResources']

                            let targetRow = getTargetBuildingRow(building_path)
                            targetRow.find(".buildingDetailsSection").html(getProgressBarHtml(building_path))
                            targetRow.find(".upgradeOrCancelBtn").html(getCnclBtnHtml(building_path))
                            initProgressBar(building_path)
                            initCancelButtons()

                        }else if(data['result'] == 'Fail'){
                            // alert("Fail")
                            console.log("WOLOLO")
                            $('#insufficentResources').modal('show')
                        }
            
                    }
                })
            })
        }
    });
}

function initCancelButtons(){

    let csrftoken = getCookie('csrftoken');

    $(".cancelUpgrade").each(function(){
        if(!$(this).data('click-init')){
            $(this).data('click-init', true)
            $(this).on('click', function(){
                let firingTime = new Date() //now
                let building_path = $(this).attr('id')
                $.ajax({
                    type: 'POST',
                    url: '/game/cancelUpgrade',
                    data: {
                        building_path: building_path,
                        village_id: villageData.village_id,
                        firingTime: firingTime,
                        csrfmiddlewaretoken: csrftoken 
                    },
                    success:function(data){
                        if(data['result'] == 'Success'){
                            console.log(data['newResources'])

                            // if(!building_path.includes('.')){
                            //     villageData.buildings[building_path] = data['newBuilding']
                            // }
                            villageData.buildings.resources = data['newResources']

                            let targetRow = getTargetBuildingRow(building_path)
                            targetRow.find(".buildingDetailsSection").html(getUpgReqHtml())
                            fillUpgReq(building_path)
                            targetRow.find(".upgradeOrCancelBtn").html(getUpgBtnHtml())
                            initUpgradeButtons()


                        }else if(data['result'] == 'Fail'){
                            // alert("Fail")
                            // console.log("WOLOLO")
                            // $('#insufficentResources').modal('show')
                        }
            
                    }
                })
            })
        }
    });
}

function displayNeededResourcesAndTimeForUpgrading(){
    let speedPercantageOfTownCenter = gameConfigs.buildings.townCenter.buildingSpeed[villageData.buildings.townCenter.level]
    //upgrading costs
    $('.upgradeBuildings').each(function(){
        let buildingName = $(this).attr('buildingName')

        if(villageData.buildings[String(buildingName)].upgrading.state == 'true'){
            initProgressBar(buildingName)
        }else{
            fillUpgReq(buildingName)
        }
    })
    $('.upgradeResources').each(function(){
        let resourceBuildingName = $(this).attr('buildingName')
        // let resourceType = $(this).attr('resourceType')
        if(villageData.buildings.resources[String(resourceBuildingName)].upgrading.state == 'true'){
            initProgressBar('resources.'+resourceBuildingName)
        }else{
            fillUpgReq("resources."+resourceBuildingName)
        }
    })
}


function initSwitchVillageDropdownButton(){
    // $("#switchVillage")
}

function initToggleVisualVillageSwitch(){
    $("#toggleVisualVillage").val('off')

    $(".toggleVisualVillage").on("change",function(){
        if(!textBasedVillageContent){let textBasedVillageContent = $(".village-content").html()}
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

function getCnclBtnHtml(building_path){
    const cnclBtnHtml = '<button class="cancelUpgrade btn btn-danger" id="'+building_path+'">Cancel</button>';
    return cnclBtnHtml;
}

function getUpgrdBtnHtml(building_path){
    const upgrdBtnHtml = '<button class="upgrade btn btn-primary" id="'+building_path+'">Upgrade</button>';
    return upgrdBtnHtml;
}