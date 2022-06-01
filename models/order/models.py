from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    """Заказ-наряд"""
    ORDER_STATUS_CHOICES = [('in_process', 'В работе'), ('completed', 'Завершен')]
    trade_point = models.ForeignKey(
        'trade_point.TradePoint', on_delete=models.PROTECT, null=False, blank=False,
        related_name='branch_orders', verbose_name='Филиал')
    contractor = models.ForeignKey(
        'contractor.Contractor', on_delete=models.PROTECT, null=False, blank=False,
        related_name='orders', verbose_name='Контрагент')
    own = models.ForeignKey(
        'own.Own', on_delete=models.PROTECT, null=False, blank=False,
        related_name='own_orders', verbose_name='Собственность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    finished_at = models.DateTimeField(null=True, blank=True,
                                       verbose_name="Дата завершения")
    status = models.CharField(max_length=100, null=False, blank=False,
                              choices=ORDER_STATUS_CHOICES, verbose_name='Статус')
    price = models.IntegerField(
        null=False, blank=False,
        validators=[MinValueValidator(0)], verbose_name='Общая сумма')
    payment = models.ForeignKey(
        'payment.Payment', on_delete=models.PROTECT, null=False,
        blank=False, related_name='payment_orders', verbose_name='Оплата')
    note = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name='Примечание')
    mileage = models.IntegerField(null=True, blank=True,
                                  validators=[MinValueValidator(0)], verbose_name='Пробег')

    def __str__(self):
        return f'{self.created_at, self.contractor, self.price, self.status}'

    class Meta:
        verbose_name = "Заказ-наряд"
        verbose_name_plural = "Заказ-наряды"
