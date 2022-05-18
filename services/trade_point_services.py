from models.trade_point.models import TradePoint
from models.organization.models import Organization
from django.shortcuts import get_object_or_404


def create_trade_point(data):
    TradePoint.objects.create(
        name=data['name'],
        address=data['address'],
        organization=get_object_or_404(Organization, id=1),
        nomenclature=data['nomenclature']
    )
