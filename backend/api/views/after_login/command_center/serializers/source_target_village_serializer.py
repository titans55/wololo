from rest_framework import serializers
from django.db.models.fields import *
from wololo.models import Villages, Users

class SourceTargetVillageIdsSerializer(serializers.Serializer):
    source_village_id = serializers.PrimaryKeyRelatedField(queryset=Villages.objects.all())
    target_village_id = serializers.PrimaryKeyRelatedField(queryset=Villages.objects.all())