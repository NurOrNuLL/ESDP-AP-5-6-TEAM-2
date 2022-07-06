from models.queue.models import Queue


class QueueService:
    @staticmethod
    def create_queue(data: dict) -> Queue:
        return Queue.objects.create(
            contractor=data['contractor'],
            own=data['own'],
            status=data['status'],
            expiration=data['expiration'],
            trade_point=data['trade_point']
        )
