from django.shortcuts import render, redirect
import urllib.request
import urllib.error
from django.contrib.auth.decorators import login_required
from wololo.commonFunctions import getGameConfig, getVillageIndex
from wololo.models import Users
from django.core.serializers.json import DjangoJSONEncoder
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt import authentication
from django.contrib.auth.models import User
from django.http import Http404

gameConfig = getGameConfig()


class PlayerProfile(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, username):
        try:
            player = Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise Http404

        player_info = player.get_player_profile_dict()

        return Response(player_info)
