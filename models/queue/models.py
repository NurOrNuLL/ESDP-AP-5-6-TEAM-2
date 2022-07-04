from django.db import models


QUEUE_STATUSES = [
    ('Актуально', 'Актуально'),
    ('Не актуально', 'Не актуально')
]


class Queue(models.Model):
    """Очередь"""
    contractor = models.ForeignKey(
        'contractor.Contractor',
        on_delete=models.PROTECT,
        related_name='contractor_queue',
        verbose_name='Контрагент',
        null=False, blank=False
    )
    own = models.ForeignKey(
        'own.Own',
        on_delete=models.PROTECT,
        related_name='own_queue',
        verbose_name='Собственность',
        null=False, blank=False
    )
    status = models.CharField(
        max_length=12, choices=QUEUE_STATUSES,
        null=False, blank=False
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата создания',
        null=False, blank=False
    )
    expiration = models.DateTimeField(
        verbose_name='Дата назначения',
        null=False, blank=False
    )
    trade_point = models.ForeignKey(
        'trade_point.TradePoint', on_delete=models.PROTECT,
        verbose_name='Филиал'
    )

    def __str__(self):
        return f'{self.created_at, self.contractor.name, self.own.name, self.status, self.expiration}'

    class Meta:
        verbose_name = "Очередь"
        verbose_name_plural = "Очередь"
