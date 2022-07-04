import json
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from celery.result import AsyncResult
from .tasks import get_report


class ReportConsumer(WebsocketConsumer):
    def connect(self) -> None:
        self.accept()

    def receive(self, text_data: str) -> None:
        data = json.loads(text_data)

        from_date = datetime.strptime(data['from_date'], '%Y-%m-%d')
        to_date = datetime.strptime(data['to_date'], '%Y-%m-%d')

        task = get_report.delay(from_date, to_date, data['tpID'])
        report = AsyncResult(task.id).get()

        self.send(json.dumps(report))
