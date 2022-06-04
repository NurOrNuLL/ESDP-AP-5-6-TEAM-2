from django.db import models

PAYMENT_STATUS_CHOICES = [('Не оплачено', 'Не оплачено'), ('Оплачено', 'Оплачено')]


class Payment(models.Model):
    """Оплата"""
    payment_status = models.CharField(max_length=100, null=False, blank=False,
                              choices=PAYMENT_STATUS_CHOICES, verbose_name='Статус оплаты')
    method = models.ForeignKey(
        'payment_method.PaymentMethod', on_delete=models.PROTECT, null=True, blank=True,
        related_name='payments', verbose_name='Способ оплаты')
    type = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f'{self.payment_status, self.method, self.type}'

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
