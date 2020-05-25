from django.shortcuts import render, redirect
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.models import Reports
import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt import authentication
from django.contrib.auth.models import User

gameConfig = getGameConfig()


class ReportsList(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, village_index=None):

        user = request.user

        if user.is_region_selected is False:
            return redirect("selectRegion")

        selected_village_index = getVillageIndex(request, user, village_index)
        if(selected_village_index is 'outOfList'):
            return redirect('myVillage')
        print(2, str(datetime.datetime.now()))

        #
        # re = Reports.objects.all()[0]
        # print(re)
        # print(re.__dict__)
        #

        reports = user.get_reports()
        print(reports)
        print(3, str(datetime.datetime.now()))

        data = {
            'user_id': user.id,
            'reports': reports,
            'unviewedReportExists': user.is_unviewed_reports_exists,
        }

        return Response(data)


###
# @login_required
# def reportsList(request, village_index=None):
#   print(0, str(datetime.datetime.now()))
#
#   user_id = request.user.id
#    user = request.user
#    if user.is_region_selected is False:
#        return redirect("selectRegion")
#
#    selected_village_index = getVillageIndex(request, user, village_index)
#    if(selected_village_index is 'outOfList'):
#        return redirect('myVillage')
#    print(2, str(datetime.datetime.now()))
#
#    #
#    # re = Reports.objects.all()[0]
#    # print(re)
#    # print(re.__dict__)
#    #
#
#    reports = user.get_reports()
#    print(reports)
#    print(3, str(datetime.datetime.now()))
#    my_villages = user.get_my_villages()
#    data = {
#        'user_id': user.id,
#        'villages_info': my_villages,
#        'selectedVillage': my_villages[selected_village_index],
#        'gameConfig': gameConfig,
#        'reports': reports,
#        'unviewedReportExists': user.is_unviewed_reports_exists,
#        'page': 'reports'
#    }
#    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
#    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
#
#    return render(request, 'reports.html', {'myVillages': my_villages, 'data': data})


class Report(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, report_index, village_index=None):

        user = request.user
        if user.is_region_selected is False:
            return redirect("selectRegion")

        selected_village_index = getVillageIndex(request, user, village_index)
        if(selected_village_index == 'outOfList'):
            return redirect('reportsList')

        print(type(report_index))
        reports = user.get_reports()
        reports[report_index]['viewed'] = True

        if user.is_unviewed_reports_exists:
            viewed_all_reports = True
            for reportElement in reports:
                if reportElement['viewed'] == False:
                    viewed_all_reports = False
                    break
            if viewed_all_reports:
                user.is_unviewed_reports_exists = False
                user.setUnviewedReportExists(False)
            user.setReports(reports)

        data = {
            'report_index': report_index,
            'user_id': user.id,
            'report': reports[report_index],
            'unviewedReportExists': user.is_unviewed_reports_exists,
        }

        return Response(data)


# def report(request, report_index, village_index=None):
#    user_id = request.user.id
#    user = request.user
#    if user.is_region_selected is False:
#        return redirect("selectRegion")
#
#    selected_village_index = getVillageIndex(request, user, village_index)
#    if(selected_village_index == 'outOfList'):
#        return redirect('reportsList')
#
#    print(type(report_index))
#    reports = user.get_reports()
#    reports[report_index]['viewed'] = True
#
#    if user.is_unviewed_reports_exists:
#        viewed_all_reports = True
#        for reportElement in reports:
#            if reportElement['viewed'] == False:
#                viewed_all_reports = False
#                break
#        if viewed_all_reports:
#            user.is_unviewed_reports_exists = False
#            user.setUnviewedReportExists(False)
#        user.setReports(reports)
#
#    my_villages = user.get_my_villages()
#    data = {
#        'report_index': report_index,
#        'user_id': user.id,
#        'villages_info': my_villages,
#        'selectedVillage': my_villages[selected_village_index],
#        'gameConfig': gameConfig,
#        'report': reports[report_index],
#        'unviewedReportExists': user.is_unviewed_reports_exists,
#        'page': 'report'
#    }
#    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
#    my_villages = json.loads(json.dumps(my_villages, cls=DjangoJSONEncoder))
#
#    return render(request, 'report.html', {'myVillages': my_villages, 'data': data})
