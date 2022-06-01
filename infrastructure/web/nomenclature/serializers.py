from rest_framework import serializers


class NomenclatureFilterSerializer(serializers.Serializer):
    search = serializers.CharField(default='')
    category = serializers.CharField(default='')
    mark = serializers.CharField(default='')
    page = serializers.IntegerField(default=1)
    limit = serializers.IntegerField()
