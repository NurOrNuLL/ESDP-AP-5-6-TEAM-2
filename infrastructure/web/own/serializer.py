from rest_framework import serializers
from models.own.models import Own


class OwnIdSerializer(serializers.Serializer):
    own_id = serializers.IntegerField(required=True)


class OwnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Own
        fields = '__all__'
