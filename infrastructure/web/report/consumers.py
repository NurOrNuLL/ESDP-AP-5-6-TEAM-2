import json
from channels.generic.websocket import WebsocketConsumer
from .tasks import get_report, get_reports_from_aws
from datetime import datetime
from celery.result import AsyncResult
from django.core.cache import cache


class ReportListConsumer(WebsocketConsumer):
    def connect(self) -> None:
        self.accept()

    def receive(self, text_data) -> None:
        tradepoint_id = json.loads(text_data)['tpID']

        task = get_reports_from_aws.delay(tradepoint_id)
        reports = json.dumps(AsyncResult(task.id).get())

        self.send(reports)


class ReportConsumer(WebsocketConsumer):
    @staticmethod
    def dates_is_valid(from_date: datetime, to_date: datetime) -> bool:
        if (to_date - from_date).days <= 366:
            return True
        return False

    def connect(self) -> None:
        self.accept()

    def receive(self, text_data: str) -> None:
        data = json.loads(text_data)

        from_date = datetime.strptime(data['from_date'], '%Y-%m-%d')
        to_date = datetime.strptime(data['to_date'], '%Y-%m-%d')

        if self.dates_is_valid(from_date, to_date):
            task = get_report.delay(from_date, to_date, int(data['report_type']), data['tpID'])
            report = AsyncResult(task.id).get()

            cache.set('report', report, 86400)

            self.send(json.dumps(report))
        else:
            error = {
                'error': 'Выберите корректные даты. Максимальный промежуток год!'
            }

            self.send(json.dumps(error))
