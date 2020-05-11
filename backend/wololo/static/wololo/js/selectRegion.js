"use strict";
var selectedRegion = null

$(function(){
    listenHoverAndClickToRegions()
})

function listenHoverAndClickToRegions(){

    $(".italy").hover(function() {
        (selectedRegion!='italy' ? $(".italy").addClass("hoverRegion") : '')
    },function() {
        (selectedRegion!='italy' ? $(".italy").removeClass("hoverRegion") : '')
    })
    $(".italy").on("click",function(){
        if(selectedRegion!='italy'){
            selectRegion('italy')
        }else{
            unselectRegion('italy')
        }  
    })
    $(".thraceAndIllyria").hover(function() {
        (selectedRegion!='thraceAndIllyria' ? $(".thraceAndIllyria").addClass("hoverRegion") : '')
    },function() {
        (selectedRegion!='thraceAndIllyria' ? $(".thraceAndIllyria").removeClass("hoverRegion") : '')
    })
    $(".thraceAndIllyria").on("click",function(){
        if(selectedRegion!='thraceAndIllyria'){
            selectRegion('thraceAndIllyria')
        }else{
            unselectRegion('thraceAndIllyria')
        }  
    })

    $(".greece").hover(function() {
        (selectedRegion!='greece' ? $(".greece").addClass("hoverRegion") : '')
    },function() {
        (selectedRegion!='greece' ? $(".greece").removeClass("hoverRegion") : '')
    })
    $(".greece").on("click",function(){
        if(selectedRegion!='greece'){
            selectRegion('greece')
        }else{
            unselectRegion('greece')
        }  
    })

    $(".anatolia").hover(function() {
        (selectedRegion!='anatolia' ? $(".anatolia").addClass("hoverRegion") : '')
    },function() {
        (selectedRegion!='anatolia' ? $(".anatolia").removeClass("hoverRegion") : '')
    })
    $(".anatolia").on("click",function(){
        if(selectedRegion!='anatolia'){
            selectRegion('anatolia')
        }else{
            unselectRegion('anatolia')
        }  
    })

    $(".levant").hover(function() {
        (selectedRegion!='levant' ? $(".levant").addClass("hoverRegion") : '')
    },function() {
        (selectedRegion!='levant' ? $(".levant").removeClass("hoverRegion") : '')
    })
    $(".levant").on("click",function(){
        if(selectedRegion!='levant'){
            selectRegion('levant')
        }else{
            unselectRegion('levant')
        }  
    })
}
function selectRegion(regionClassName){
    $("."+regionClassName).removeClass("hoverRegion")
    $("path").removeClass('selectedRegion')
    $("."+regionClassName).addClass('selectedRegion')
    selectedRegion = regionClassName
    console.log(regionClassName, "selected")
    if(regionClassName=='italy'){
        $(".selectingRegionText").html("Your first village will be located at <b><i>Italy</i></b>.")
    }else if(regionClassName=='thraceAndIllyria'){
        $(".selectingRegionText").html("Your first village will be located at <b><i>Thrace & Illyria</i></b>.")
    }else if(regionClassName=='greece'){
        $(".selectingRegionText").html("Your first village will be located at <b><i>Greece</i></b>.")
    }else if(regionClassName=='anatolia'){
        $(".selectingRegionText").html("Your first village will be located at <b><i>Anatolia</i></b>.")
    }else if(regionClassName=='levant'){
        $(".selectingRegionText").html("Your first village will be located at <b><i>Levant</i></b>.")
    }
    $("#confirmRegion").removeClass("disabled")
    $("#selectedRegionInput").attr("value", regionClassName)
}
function unselectRegion(regionClassName){
    selectedRegion = null
    $("#selectedRegionInput").attr("value", "")
    $("."+regionClassName).removeClass('selectedRegion')
    $(".selectingRegionText").html("Choose the region of your first village.")
    $("#confirmRegion").addClass("disabled")
}