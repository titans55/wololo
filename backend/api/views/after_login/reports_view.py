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
from rest_framework import generics
from wololo.models import Reports
from api.viewset_serializers import ReportsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from wololo.models import Reports
from django.http import Http404

gameConfig = getGameConfig()


class ReportsList(generics.ListAPIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields=['id', 'type']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sended_to_user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super(ReportsList, self).list(request, args, kwargs)
        response.data['current_page_number'] = self.paginator.page.number
        response.data['paginate_by'] = self.paginator.page_size
        return response


class ReportViewed(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, report_id):
        try:
            Reports.objects.filter(id=report_id).update(is_viewed=True)
        except Reports.DoesNotExist:
            raise Http404
        return Response()
