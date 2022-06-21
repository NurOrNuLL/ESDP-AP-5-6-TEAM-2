from models.trade_point.models import TradePoint
from models.organization.models import Organization
from django.shortcuts import get_object_or_404
from typing import List


class TradePointServices:
    @staticmethod
    def create_trade_point(data: dict) -> None:
        TradePoint.objects.create(
            name=data['name'],
            address=data['address'],
            organization=get_object_or_404(Organization, id=1),
            nomenclature=data['nomenclature']
        )

    @staticmethod
    def get_trade_points(kwargs: dict) -> List['TradePoint']:
        return TradePoint.objects.filter(organization=kwargs['orgID'])

    @staticmethod
    def get_trade_point_by_id(kwargs: dict) -> TradePoint:
        return TradePoint.objects.get(id=kwargs['tpID'])

    @staticmethod
    def get_trade_point_from_form(kwargs: dict) -> TradePoint:
        return TradePoint.objects.get(id=kwargs['tradepoint'].id)
