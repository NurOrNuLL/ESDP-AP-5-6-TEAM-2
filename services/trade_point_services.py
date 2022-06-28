from models.trade_point.models import TradePoint
from models.organization.models import Organization
from django.shortcuts import get_object_or_404
from typing import List

from services.nomenclature_services import NomenclatureService


class TradePointServices:
    @staticmethod
    def create_trade_point(data: dict) -> None:
        trade_point = TradePoint.objects.create(
            name=data['name'],
            address=data['address'],
            organization=get_object_or_404(Organization, id=1)
        )
        trade_point.nomenclature.set(data['nomenclature'])

    @staticmethod
    def get_trade_points(kwargs: dict) -> List['TradePoint']:
        return TradePoint.objects.filter(organization=kwargs['orgID'])

    @staticmethod
    def get_trade_point_by_id(kwargs: dict) -> TradePoint:
        return TradePoint.objects.get(id=kwargs['tpID'])

    @staticmethod
    def get_trade_point_from_form(kwargs: dict) -> TradePoint:
        return TradePoint.objects.get(id=kwargs['tradepoint'].id)
      
    @staticmethod
    def get_trade_point_by_clean_id(tpID: dict) -> TradePoint:
        return TradePoint.objects.get(id=tpID)

    @staticmethod
    def update_trade_point(trade_point: TradePoint, data: dict) -> TradePoint:
        trade_point.name = data['name']
        trade_point.address = data['address']
        trade_point.save()
        trade_point.nomenclature.set(data['nomenclature'])
        return trade_point
