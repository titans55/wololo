$(function(){
    initInVillageTroopMarker()
})

function initInVillageTroopMarker(){
    $(".inVillageTroopMarker").not(".disabled").on("click", function(){
        console.log($(this), " wololo")
        let totalAmount = parseInt($(this).find(".troopAmount").html())
        $(this).siblings(".troopsToSend").val(totalAmount).change();
    })
}