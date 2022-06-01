from django.db import models


class Payment(models.Model):
    """Оплата"""
    PAYMENT_STATUS_CHOICES = [('paid', 'Оплачено'), ('not_paid', 'Не оплачено')]
    status = models.CharField(max_length=100, null=False, blank=False,
                              choices=PAYMENT_STATUS_CHOICES, verbose_name='Статус оплаты')
    method = models.ForeignKey(
        'payment_method.PaymentMethod', on_delete=models.PROTECT, null=True, blank=True,
        related_name='payments', verbose_name='Способ оплаты')
    type = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f'{self.status, self.method, self.type}'

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
