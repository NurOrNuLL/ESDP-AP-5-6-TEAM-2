from django.db import models


class PaymentMethod(models.Model):
    """Способ оплаты"""
    name = models.CharField(max_length=100, null=False,
                            blank=False, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"
