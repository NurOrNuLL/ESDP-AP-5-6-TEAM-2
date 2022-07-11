from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class OrderStatusUpdateTrackingConsumer(WebsocketConsumer):
    def connect(self) -> None:
        async_to_sync(self.channel_layer.group_add)('orderStatuses', self.channel_name)

        self.accept()

    def update_status(self, signal_data: dict) -> None:
        data = signal_data

        self.send(json.dumps(data))

    def disconnect(self, code) -> None:
        async_to_sync(self.channel_layer.group_discard)('orderStatuses', self.channel_name)
