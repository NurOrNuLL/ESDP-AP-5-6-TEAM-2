from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    tpID = serializers.IntegerField()
