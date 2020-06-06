from django.shortcuts import render, redirect
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from django.core.serializers.json import DjangoJSONEncoder
import json
from wololo.models import Villages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt import authentication
from django.contrib.auth.models import User
from django.http import Http404

gameConfig = getGameConfig()


class VillageProfile(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, village_id):
        try:
            village = Villages.objects.get(id=village_id)
        except Villages.objects.DoesNotExist:
            raise Http404
        village_info = village.get_village_profile_dict()

        return Response(village_info)