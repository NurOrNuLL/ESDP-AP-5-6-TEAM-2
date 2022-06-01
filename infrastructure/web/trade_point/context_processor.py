from typing import Dict
from models.trade_point.models import TradePoint


def trade_point_context(request) -> Dict[object, TradePoint]:
    trade_points = TradePoint.objects.all()
    return {
        'trade_points': trade_points
    }
