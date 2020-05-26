from rest_framework import serializers
from django.db.models.fields import *
from wololo.models import Users

class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'id', 
            'username', 
            'number_of_villages', 
            'points',
            'ranking'
        )