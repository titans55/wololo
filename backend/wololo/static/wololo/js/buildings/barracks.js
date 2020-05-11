"use strict";
var village_id
var gameConfigs = JSON.parse(($("#gameConfigData").attr("data")).replace(/'/g, '"'))
var villageData = JSON.parse(($("#villageDataJSON").attr("data")).replace(/'/g, '"'))
$(function(){
    village_id = villageData.village_id
    displayNeededTimeForInfantryUnits()
    initTrainUnitsButton()
    initTrainingQueue()
    trainUnitQuantityFormControl()
})

function displayNeededTimeForInfantryUnits(){
    for(let [unitName, units] of Object.entries(gameConfigs.units.infantry)){
        units.neededTrainingBaseTime
        
    };

    $(".neededTime").each(function(){
        const unitName = $(this).attr("unitName");
        const baseTrainingTime = gameConfigs.units.infantry[unitName].neededTrainingBaseTime
        const barracksLevel = villageData.buildings.barracks.level
        const speedPercantageOfBarracks = gameConfigs.buildings.barracks.trainingSpeed[barracksLevel]
        const neededTrainingTime = calculateTimeFromMinutes(lowerByPercantage(baseTrainingTime, speedPercantageOfBarracks))
        $(this).html(neededTrainingTime)
    })
}

function initTrainUnitsButton(){
    let csrftoken = getCookie('csrftoken');
    $("#trainUnits").on('click', function(){
        let firingTime = new Date() //now
        let unitName, value
        let unitType = 'infantry'
        $(".unitsToTrainValue").each(function(){
            if($(this).val()>0){
                unitName = $(this).attr('unitName')
                value = $(this).val()
            }
        })
        if(value > 0){
            $.ajax({
                type: 'POST',
                url: '/game/barracks/trainUnits',
                data: {
                    firingTime: firingTime,
                    village_id: village_id,
                    unitType: unitType,
                    unitName: unitName,
                    value: value,
                    csrfmiddlewaretoken: csrftoken ,
                },
                success:function(data){
                    if(data['result'] == 'Success'){
                        villageData.buildings.resources = data['newResources']
                        let newQueueElement = data['newQueueElement']

                        if($(".queueElements").length){
                            $(".queueElements").append(getQueueElementRowHtml(
                                newQueueElement['unitsLeft'], newQueueElement['unitName'], newQueueElement['willEndAt']
                            ))
                        }else{
                            $(".trainingQueueHolder").html(getTrainingQueueTableHtml())
                            $(".queueElements").append(getQueueElementRowHtml(
                                newQueueElement['unitsLeft'], newQueueElement['unitName'], newQueueElement['willEndAt']
                            ))
                        }
                        initTrainingQueue()                        
                        console.log("started to training")
                        
                    }else if(data['result'] == 'Fail'){
                        alert("Insufficent Resources!")
                      
                    }
    
                }
            })
        }else{
            alert("You must train at least 1 unit.")
        }
    })
}

function initTrainingQueue(){
    if($("#trainingQueue").length){
        console.log("yes")

        $(".queueElement").each(function(){
            let queueElement = $(this)
            if(!queueElement.data("queue-init")){
                console.log(queueElement, "wololo")
                let willEndAt = moment(queueElement.find(".willEndAt").html())
                queueElement.find(".willEndAt").html(willEndAt.format("DD-MM-YYYY HH:mm:ss:SSS")) //or .toString()
                tick(queueElement, willEndAt)
                let interval = setInterval(() => {
                    let cntdwn = tick(queueElement, willEndAt)
                    if(cntdwn.split(':')[0] == '00' && cntdwn.split(':')[1] == '00' && cntdwn.split(':')[2] == '00'){
                        alert("stopped")
                        clearInterval(interval)
                    }
                },1000)
                queueElement.data("queue-init", true)
            }
        })

        function tick(queueElement, willEndAt){
            let now = moment(new Date())
            let countdown = moment(willEndAt.diff(now)).subtract({ hours: 2}).format("HH:mm:ss")//* TIME ZONE PROBLEM *//
            queueElement.find(".timeLeft").html(countdown)
            return countdown
        }
    }
}

function trainUnitQuantityFormControl(){
    $(".trainUnitRow").each(function(){
        let unitRow = $(this)
        let requiredWood = parseInt(unitRow.find(".required-Wood").attr("amount"))
        let requiredIron = parseInt(unitRow.find(".required-Iron").attr("amount"))
        let requiredClay = parseInt(unitRow.find(".required-Clay").attr("amount"))
        let requiredPop = parseInt(unitRow.find(".required-pop").attr("amount"))

        unitRow.find(".unitsToTrainValue").bind("keyup change", function(){
            let val = parseInt($(this).val())
            if(val>1){
                unitRow.find(".required-Wood").html(requiredWood*val+"<div>Wood</div>")
                // (parseInt($("#wood").html()) <= requiredWood*val ? unitRow.find(".required-Wood").addClass('text-danger') : unitRow.find(".required-Wood").removeClass('text-danger'))
                unitRow.find(".required-Iron").html(requiredIron*val+"<div>Iron</div>")
                unitRow.find(".required-Clay").html(requiredClay*val+"<div>Clay</div>")
                unitRow.find(".required-pop").html(requiredPop*val+"<div>Population</div>")
            }else{
                unitRow.find(".required-Wood").html(requiredWood+"<div>Wood</div>")
                unitRow.find(".required-Iron").html(requiredIron+"<div>Iron</div>")
                unitRow.find(".required-Clay").html(requiredClay+"<div>Clay</div>")
                unitRow.find(".required-pop").html(requiredPop+"<div>Population</div>")
            }
        })
    })
}

function getQueueElementRowHtml(unitsLeft, unitName, willEndAt){
    const queueElementToAppend = '<tr class="queueElement">' +
        '<td class="unitsLeft">' + unitsLeft + ' ' + unitName + '</td>' +
        '<td class="willEndAt">' + willEndAt + '</td>' +
        '<td class="timeLeft">' + 'X' + '</td>' +
    '</tr>';

    return queueElementToAppend;
}

function getTrainingQueueTableHtml(){
    const trainingQueueTable = '<table class="table text-center" id="trainingQueue">' +
        '<thead>' +
            '<tr>' +
                '<th scope="col">Unit Name</th>' +
                '<th scope="col">Will End At</th>' +
                '<th scope="col">Time Left</th>' +
            '</tr>' +
        '</thead>' +
        '<tbody class="queueElements">' +
        '</tbody>' +
    '</table>';

    return trainingQueueTable;
}