from rest_framework import serializers
from models.order.models import Order
from models.payment.models import Payment
from models.contractor.models import Contractor
from models.own.models import Own


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'


class OwnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Own
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    contractor = ContractorSerializer(read_only=True)
    own = OwnSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
