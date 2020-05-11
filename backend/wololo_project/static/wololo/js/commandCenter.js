$(function(){
    initInVillageTroopMarker()
    updateTroopsFormInput()
})

function initInVillageTroopMarker(){
    $(".inVillageTroopMarker").not(".disabled").on("click", function(){
        console.log($(this), " wololo")
        let totalAmount = parseInt($(this).find(".troopAmount").html())
        $(this).siblings(".troopsToSend").val(totalAmount).change();
    })
}

function updateTroopsFormInput(){
    $(".troopsToSend").on("change", function(){
        let troopsToSend = {}
        $(this).each(function(){
            if(parseInt($(this).val())>0){
                const unitType = $(this).attr("unitType")
                const unitName = $(this).attr("unitName")
                troopsToSend = {}
                troopsToSend[unitType] = {}
                troopsToSend[unitType][unitName] = parseInt($(this).val())
                
            }
        })
        $(".troops-form-input").val(JSON.stringify(troopsToSend))
    })
}