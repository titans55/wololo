from rest_framework import serializers
from django.db.models.fields import *
from wololo.models import Villages, Users
from api.serializers import VillagesSerializer

class UnitToTrainSerializer(serializers.Serializer):
    unit_name = CharField()
    amount = IntegerField()

    class Meta:
        fields = (
            'unit_name', 
            'amount',  
        )

class UnitsToTrainSerializer(serializers.Serializer):
    village_id = serializers.PrimaryKeyRelatedField(queryset=Villages.objects.all())
    units_to_train = serializers.ListField(child=UnitToTrainSerializer())

    class Meta:
        fields = (
            'units_to_train', 
        )
