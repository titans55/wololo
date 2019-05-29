"use strict";

$(function(){
    console.log("ranking.js loaded")

    $.extend( true, $.fn.dataTable.defaults, {
        "ordering": false
    } );

    $('#example').DataTable();

})