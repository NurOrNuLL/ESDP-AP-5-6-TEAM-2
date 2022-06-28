from rest_framework import serializers
from models.nomenclature.models import Nomenclature


class NomenclatureFilterSerializer(serializers.Serializer):
    search = serializers.CharField(default='')
    category = serializers.CharField(default='')
    mark = serializers.CharField(default='')
    page = serializers.IntegerField(default=1)
    limit = serializers.IntegerField()


class NomenclatureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nomenclature
        fields = ['name', 'version']
