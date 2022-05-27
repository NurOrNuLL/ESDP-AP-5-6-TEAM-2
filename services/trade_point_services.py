from models.trade_point.models import TradePoint
from models.organization.models import Organization
from django.shortcuts import get_object_or_404


class TradePointServices:
    @staticmethod
    def create_trade_point(data: dict) -> None:
        TradePoint.objects.create(
            name=data['name'],
            address=data['address'],
            organization=get_object_or_404(Organization, id=1),
            nomenclature=data['nomenclature']
        )
