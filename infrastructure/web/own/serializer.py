from rest_framework import serializers


class OwnSerializer(serializers.Serializer):
    own_id = serializers.IntegerField(required=True)
