from django.db import models


class Report(models.Model):
    report_uuid = models.UUIDField(editable=False, verbose_name='Отчет')
    tradepoint_id = models.PositiveIntegerField(verbose_name='Филиал')
