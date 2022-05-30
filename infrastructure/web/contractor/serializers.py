from rest_framework import serializers
from models.contractor.models import Contractor


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'

