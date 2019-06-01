from django.shortcuts import render, redirect
from wololo.firebaseUser import firebaseUser
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.helperFunctions import getUsernameByUserID, getVillagenameByVillageID
import datetime

gameConfig = getGameConfig()

@login_required    
def reportsList(request, village_index=None):
    print (0, str(datetime.datetime.now()))

    user_id = request.user.id
    user = request.user
    if user.is_region_selected is False :
        return redirect("selectRegion")
       
    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index is 'outOfList'):
        return redirect('myVillage')
    print (2, str(datetime.datetime.now()))


    reports = user.getReports()
    print (3, str(datetime.datetime.now()))

    data = {
        'user_id' : user.id,
        'villages_info' : user.myVillages,
        'selectedVillage': user.myVillages[selected_village_index],
        'gameConfig' : gameConfig,
        'reports' : reports,
        'unviewedReportExists' : user.unviewedReportExists,
        'page' : 'reports'
    }

    return render(request, 'reports.html', {'myVillages':user.myVillages, 'data' : data})

def report(request, report_index, village_index=None):
    user_id = request.user.id
    user = request.user
    if user.regionSelected is False :
        return redirect("selectRegion")

    selected_village_index = getVillageIndex(request, user, village_index)
    if(selected_village_index == 'outOfList'):
        return redirect('reportsList')


    reports = user.getReports()
    reports[report_index]['viewed'] = True

    if user.unviewedReportExists:
        viewedAllReports = True
        for reportElement in reports:
            if reportElement['viewed'] == False:
                viewedAllReports = False
                break
        if viewedAllReports:
            user.unviewedReportExists = False
            user.setUnviewedReportExists(False)
        user.setReports(reports)


    data = {
        'report_index' : report_index,
        'user_id' : user.id,
        'villages_info' : user.myVillages,
        'selectedVillage': user.myVillages[selected_village_index],
        'gameConfig' : gameConfig,
        'report' : reports[report_index],
        'unviewedReportExists' : user.unviewedReportExists,
        'page' : 'report'
    }

    return render(request, 'report.html', {'myVillages':user.myVillages, 'data' : data})
